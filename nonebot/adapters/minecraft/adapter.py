import json
import asyncio
import inspect
import contextlib
from typing import Any, Dict, Optional, Generator, Type, List

from aiomcrcon import (
    Client as RCONClient,
    RCONConnectionError as BaseRCONConnectionError,
    IncorrectPasswordError as BaseIncorrectPasswordError,
    ClientNotConnectedError as BaseClientNotConnectedError,
)
from nonebot import get_plugin_config
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.compat import type_validate_python
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    ASGIMixin,
    WebSocket,
    WebSocketServerSetup,
    WebSocketClientMixin,
)
from nonebot.exception import WebSocketClosed
from nonebot.typing import overrides
from nonebot.utils import escape_tag

from .model import (
    MessageList,
    SendTitleItem,
    SendTitleBody,
    SendActionBarBody,
    WebSocketSendBody,
)

from . import event
from .bot import Bot
from .event import Event
from .config import Config
from .collator import Collator
from .utils import log, get_msg, get_actionbar_msg
from .exception import (
    IncorrectPasswordError,
    ClientNotConnectedError,
    RCONConnectionError,
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
        headers = {"x-self-name": "".join(f"\\u{ord(c):04x}" for c in server_name)}
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
                        bot = Bot(self, server_name, rcon)
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
        log("DEBUG", f"Calling API <y>{api}</y>")
        if websocket:
            websocket_send_body = WebSocketSendBody()
            if api == "send_msg":
                websocket_send_body.api = "broadcast"
                websocket_send_body.data = MessageList(message_list=get_msg(**data))
            elif api == "send_title":
                websocket_send_body.api = "send_title"
                send_title_item = SendTitleItem(
                    title=data.get("title"),
                    subtitle=data.get("subtitle"),
                    fadein=data.get("fadein") if data.get("fadein") else 10,
                    stay=data.get("stay") if data.get("stay") else 70,
                    fadeout=data.get("fadeout") if data.get("fadeout") else 20,
                )
                websocket_send_body.data = SendTitleBody(send_title=send_title_item)
            elif api == "send_actionbar":
                websocket_send_body.api = "actionbar"
                websocket_send_body.data = SendActionBarBody(
                    message_list=get_actionbar_msg(**data)
                )
            elif api == "send_rcon_cmd":
                try:
                    return await bot.rcon.send_cmd(data.get("command"))
                except BaseClientNotConnectedError:
                    raise ClientNotConnectedError()

            await websocket.send(websocket_send_body.model_dump_json())
        return

    async def _connect_rcon(self, server_name: str, server_host: str) -> Optional[RCONClient]:
        if server := self.minecraft_config.minecraft_server_rcon.get(server_name):
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

        self_id = ori_self_id.encode("utf-8").decode("unicode_escape")

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

        bot = Bot(self, self_id, rcon)
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
