import json
import urllib
import asyncio
import inspect
import contextlib
from typing import Any, Dict, List, Type, Optional, Generator

from nonebot.typing import overrides
from nonebot.utils import escape_tag
from aiomcrcon import Client as RCONClient
from nonebot.exception import WebSocketClosed
from nonebot.compat import type_validate_python
from aiomcrcon import RCONConnectionError as BaseRCONConnectionError
from aiomcrcon import IncorrectPasswordError as BaseIncorrectPasswordError
from aiomcrcon import ClientNotConnectedError as BaseClientNotConnectedError
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    ASGIMixin,
    WebSocket,
    WebSocketClientMixin,
    WebSocketServerSetup,
)

from nonebot import get_plugin_config
from nonebot.adapters import Adapter as BaseAdapter

from . import event
from .bot import Bot
from .event import Event
from .config import Config
from .collator import Collator
from .store import ResultStore
from .utils import DataclassEncoder, log, zip_dict, handle_api_result
from .exception import (
    NetworkError,
    RCONConnectionError,
    IncorrectPasswordError,
    ClientNotConnectedError,
)

RECONNECT_INTERVAL = 3.0
DEFAULT_MODELS: List[Type[Event]] = []
for model_name in dir(event):
    model = getattr(event, model_name)
    if not inspect.isclass(model) or not issubclass(model, Event):
        continue
    DEFAULT_MODELS.append(model)


class Adapter(BaseAdapter):
    event_models = Collator(
        "Minecraft",
        DEFAULT_MODELS,
        (
            "post_type",
            "event_name",
            # "sub_type",
        ),
    )

    _result_store = ResultStore()

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.minecraft_config: Config = get_plugin_config(Config)
        self.connections: Dict[str, WebSocket] = {}
        self.tasks: List["asyncio.Task"] = []
        self._setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "Minecraft"

    def _setup(self) -> None:
        if isinstance(self.driver, ASGIMixin):
            ws_setup = WebSocketServerSetup(
                URL("/minecraft/"), f"{self.get_name()} WS", self._handle_ws
            )
            self.setup_websocket_server(ws_setup)
            ws_setup = WebSocketServerSetup(
                URL("/minecraft/ws"), f"{self.get_name()} WS", self._handle_ws
            )
            self.setup_websocket_server(ws_setup)
            ws_setup = WebSocketServerSetup(
                URL("/minecraft/ws/"), f"{self.get_name()} WS", self._handle_ws
            )
            self.setup_websocket_server(ws_setup)

        if self.minecraft_config.minecraft_ws_urls:
            if not isinstance(self.driver, WebSocketClientMixin):
                log(
                    "WARNING",
                    (
                        f"Current driver {self.config.driver} does not support "
                        "websocket client connections! Ignored"
                    ),
                )
            else:
                self.on_ready(self._start_forward)
                self.driver.on_shutdown(self._stop_forward)

    async def _start_forward(self) -> None:
        for server_name in self.minecraft_config.minecraft_ws_urls.keys():
            for url in self.minecraft_config.minecraft_ws_urls[server_name]:
                try:
                    ws_url = URL(url)
                    self.tasks.append(
                        asyncio.create_task(self._forward_ws(server_name, ws_url))
                    )
                except Exception as e:
                    log(
                        "ERROR",
                        f"<r><bg #f8bbd0>Bad url {escape_tag(url)} "
                        "in minecraft forward websocket config</bg #f8bbd0></r>",
                        e,
                    )

    async def _stop_forward(self) -> None:
        for task in self.tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def _forward_ws(self, server_name: str, url: URL) -> None:
        assert url.host is not None
        headers = {
            "x-self-name": urllib.parse.quote_plus(server_name), # type: ignore
            "x-client-origin": "nonebot",
        }
        if self.minecraft_config.minecraft_access_token:
            headers["Authorization"] = (
                f"Bearer {self.minecraft_config.minecraft_access_token}"
            )
        request = Request("GET", url, headers=headers, timeout=30.0)

        bot: Optional[Bot] = None

        while True:
            try:
                async with self.websocket(request) as ws:
                    log(
                        "DEBUG",
                        f"WebSocket Connection to {escape_tag(str(url))} established",
                    )
                    # 连接 Rcon
                    rcon = await self._connect_rcon(server_name, url.host)
                    if not bot:
                        bot = Bot(self, server_name, rcon) # type: ignore
                        self.bot_connect(bot)
                        self.connections[server_name] = ws
                        log(
                            "INFO",
                            f"<y>Bot {escape_tag(server_name)}</y> connected",
                        )
                    try:
                        while True:
                            data = await ws.receive()
                            json_data = json.loads(data)
                            event = self.json_to_event(json_data)
                            if not event:
                                continue
                            asyncio.create_task(bot.handle_event(event))
                    except WebSocketClosed as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>WebSocket Closed</bg #f8bbd0></r>",
                            e,
                        )
                    except Exception as e:
                        log(
                            "ERROR",
                            (
                                "<r><bg #f8bbd0>"
                                "Error while process data from websocket"
                                f"{escape_tag(str(url))}. Trying to reconnect..."
                                "</bg #f8bbd0></r>"
                            ),
                            e,
                        )
                    finally:
                        if bot:
                            if rcon:
                                await rcon.close()
                            self.connections.pop(bot.self_id, None)
                            self.bot_disconnect(bot)
                            bot = None

            except Exception as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while setup websocket to "
                    f"{escape_tag(str(url))}. Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )

            await asyncio.sleep(RECONNECT_INTERVAL)

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        websocket = self.connections.get(bot.self_id, None)
        timeout: float = data.get("_timeout", self.config.api_timeout)
        log("DEBUG", f"Calling API <y>{api}</y>")
        if websocket:
            if api == "send_rcon_cmd":
                try:
                    if bot.rcon is None:
                        raise RCONConnectionError(msg="RCON client is None")
                    return await bot.rcon.send_cmd( # type: ignore
                        cmd=data.get("command"),
                        timeout=timeout
                    )
                except BaseClientNotConnectedError:
                    raise ClientNotConnectedError()
                except Exception as e:
                    raise RCONConnectionError(msg=str(e), error=e)
            seq = self._result_store.get_seq()
            json_data = json.dumps(
                {"api": api, "data": zip_dict(data), "echo": str(seq)},
                cls=DataclassEncoder
            )
            await websocket.send(json_data)
            try:
                return handle_api_result(await self._result_store.fetch(seq, timeout))
            except asyncio.TimeoutError:
                raise NetworkError(f"WebSocket call api {api} timeout") from None

    async def _connect_rcon(self, server_name: str, server_host: str) -> Optional[RCONClient]:
        if server := self.minecraft_config.minecraft_server_rcon.get(server_name):
            server_host = server.rcon_host or server_host
            rcon = RCONClient(
                server_host,
                server.rcon_port,
                server.rcon_password,
            )
            if server.enable_rcon:
                log(
                    "INFO",
                    f"<y>Connecting</y> RCON for <y>Bot {escape_tag(server_name)}</y>",
                )
                try:
                    await rcon.connect(timeout=server.timeout)
                except BaseIncorrectPasswordError:
                    raise IncorrectPasswordError()
                except BaseClientNotConnectedError:
                    raise ClientNotConnectedError()
                except BaseRCONConnectionError as e:
                    raise RCONConnectionError(e.message, e.error)
                else:
                    log(
                        "INFO",
                        f"RCON for <y>Bot {escape_tag(server_name)}</y> <g>connected</g>",
                    )
                    return rcon
            else:
                log(
                    "INFO",
                    f"RCON for <y>Bot {escape_tag(server_name)}</y> is not enabled, will not connect",
                )
        else:
            log(
                "INFO",
                f"RCON configuration for <y>Bot {escape_tag(server_name)}</y> not found, will not connect",
            )
        return None

    async def _handle_ws(self, websocket: WebSocket) -> None:
        ori_self_id = websocket.request.headers.get("x-self-name")

        # check ori_self_id
        if not ori_self_id:
            log("WARNING", "Missing X-Self-Name Header")
            await websocket.close(1008, "Missing X-Self-Name Header")
            return

        if client_origin := websocket.request.headers.get("x-client-origin"):
            if client_origin == "nonebot":
                log("WARNING", "X-Client-Origin Header cannot be nonebot")
                await websocket.close(1008, "X-Client-Origin Header cannot be nonebot")
                return

        self_id = urllib.parse.unquote_plus(ori_self_id) # type: ignore

        if self.minecraft_config.minecraft_access_token:
            access_token = websocket.request.headers.get("Authorization")
            if not access_token:
                log("WARNING", "Missing Authorization Header")
                await websocket.close(1008, "Missing Authorization Header")
                return

            if access_token != "Bearer " + self.minecraft_config.minecraft_access_token:
                log("WARNING", "Invalid Authorization Header")
                await websocket.close(1008, "Invalid Authorization Header")
                return

        if self_id in self.bots:
            log("WARNING", f"There's already a bot {self_id}, ignored")
            await websocket.close(1008, "Duplicate X-Self-Name")
            return

        await websocket.accept()

        rcon = await self._connect_rcon(self_id, websocket.__dict__["websocket"].__dict__["scope"]["client"][0])

        bot = Bot(self, self_id, rcon) # type: ignore
        self.connections[self_id] = websocket
        self.bot_connect(bot)

        log("INFO", f"<y>Bot {escape_tag(self_id)}</y> connected")

        try:
            while True:
                data = await websocket.receive()
                json_data = json.loads(data)
                if event := self.json_to_event(json_data, self_id):
                    asyncio.create_task(bot.handle_event(event))
        except WebSocketClosed:
            log("WARNING", f"WebSocket for Bot {escape_tag(self_id)} closed by peer")
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Error while process data from websocket "
                f"for bot {escape_tag(self_id)}.</bg #f8bbd0></r>",
                e,
            )
        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
                if rcon:
                    await rcon.close()
                    log("INFO", f"RCON for <y>Bot {escape_tag(self_id)}</y> closed")
            self.connections.pop(self_id, None)
            self.bot_disconnect(bot)

    @classmethod
    def add_custom_model(cls, *model: Type[Event]) -> None:
        """插入或覆盖一个自定义的 Event 类型。

        参数:
            model: 自定义的 Event 类型
        """
        cls.event_models.add_model(*model)

    @classmethod
    def get_event_model(
            cls, data: Dict[str, Any]
    ) -> Generator[Type[Event], None, None]:
        """根据事件获取对应 `Event Model` 及 `FallBack Event Model` 列表。"""
        yield from cls.event_models.get_model(data)

    @classmethod
    def json_to_event(
            cls, json_data: Any, self_id: Optional[str] = None
    ) -> Optional[Event]:
        """将 json 数据转换为 Event 对象。

        如果为 API 调用返回数据且提供了 Event 对应 Bot，则将数据存入 ResultStore。

        参数:
            json_data: json 数据
            self_id: 当前 Event 对应的 Bot

        返回:
            Event 对象，如果解析失败或为 API 调用返回数据，则返回 None
        """
        if not isinstance(json_data, dict):
            return None

        if json_data.get("post_type") == "response":
            cls._result_store.add_result(json_data)
            return

        try:
            for model in cls.get_event_model(json_data):
                try:
                    event = type_validate_python(model, json_data)
                    break
                except Exception as e:
                    log("DEBUG", "Event Parser Error", e)
            else:
                event = type_validate_python(Event, json_data)

            return event
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Failed to parse event. "
                f"Raw: {escape_tag(str(json_data))}</bg #f8bbd0></r>",
                e,
            )
