import asyncio
import json

from fakes import FakeWebSocket
import nonebot
from nonebot.adapters.minecraft import Adapter, Bot, Message, MessageSegment
from nonebot.adapters.minecraft.exception import ActionFailed, ApiNotAvailable, NetworkError
from nonebot.adapters.minecraft.models import Status
from nonebot.adapters.minecraft.store import ResultStore
from nonebug import App
import pytest

STATUS_DATA = {
    "timestamp": 1775444822691,
    "server_type": "forge",
    "server_version": "1.21",
    "server_list_ping": {
        "available": True,
        "host": "127.0.0.1",
        "port": 25565,
        "reason": "ok",
        "error": None,
        "version": {
            "name": "1.21",
            "protocol": 767.0,
        },
        "players": {
            "max": 20.0,
            "online": 0.0,
        },
        "description": {"text": "A Minecraft Server"},
        "favicon": None,
        "enforcesSecureChat": True,
    },
    "cpu_information": {
        "cpu_cores": 16,
        "load_average": -1.0,
        "system_load": 0.0,
        "process_load": -1.0,
    },
    "memory_information": {
        "physical_memory": {
            "total": 34278875136,
            "free": 14827216896,
            "used": 19451658240,
            "percentage": 56.75,
        },
        "jvm_memory": {
            "total": 486539264,
            "free": 95978912,
            "max": 8573157376,
            "used": 390560352,
            "percentage": 4.56,
        },
    },
}


class FakeAdapter:
    def __init__(self):
        self.calls = []
        self.status = STATUS_DATA

    async def send_websocket_message(self, bot_id, api, data=None):
        self.calls.append((bot_id, api, data))
        if api == "send_rcon_command":
            return "command result"
        if api == "get_status":
            return self.status
        return None


def make_bot():
    return Bot(FakeAdapter(), "Server")


@pytest.mark.asyncio
async def test_send_msg_serializes_string():
    bot = make_bot()

    await Bot.send_msg(bot, "hello")

    assert bot.adapter.calls == [("Server", "send_msg", {"message": {"text": "hello"}})]


@pytest.mark.asyncio
async def test_send_msg_serializes_message():
    bot = make_bot()
    message = Message([MessageSegment.text("hello"), MessageSegment.text("world", color="gold")])

    await Bot.send_msg(bot, message)

    assert bot.adapter.calls == [
        (
            "Server",
            "send_msg",
            {"message": [{"text": "hello"}, {"text": "world", "color": "gold"}]},
        )
    ]


@pytest.mark.asyncio
async def test_send_title_requires_title_or_subtitle():
    bot = make_bot()

    with pytest.raises(ActionFailed):
        await Bot.send_title(bot)


@pytest.mark.asyncio
async def test_send_title_serializes_payload():
    bot = make_bot()

    await Bot.send_title(bot, title="title", subtitle=MessageSegment.text("subtitle"), fade_in=1, stay=2, fade_out=3)

    assert bot.adapter.calls == [
        (
            "Server",
            "send_title",
            {
                "title": {"text": "title"},
                "subtitle": {"text": "subtitle"},
                "fade_in": 1,
                "stay": 2,
                "fade_out": 3,
            },
        )
    ]


@pytest.mark.asyncio
async def test_send_actionbar_serializes_message_segment():
    bot = make_bot()

    await Bot.send_actionbar(bot, MessageSegment.text("action", bold=True))

    assert bot.adapter.calls == [("Server", "send_actionbar", {"message": {"text": "action", "bold": True}})]


@pytest.mark.asyncio
async def test_send_rcon_command_returns_result():
    bot = make_bot()

    result = await Bot.send_rcon_command(bot, "list")

    assert result == "command result"
    assert bot.adapter.calls == [("Server", "send_rcon_command", {"command": "list"})]


@pytest.mark.asyncio
async def test_get_status_returns_status():
    bot = make_bot()

    result = await Bot.get_status(bot)

    assert isinstance(result, Status)
    assert result.timestamp == 1775444822691
    assert result.server_type == "forge"
    assert result.server_list_ping.reason == "ok"
    assert result.server_list_ping.description == {"text": "A Minecraft Server"}
    assert getattr(result.server_list_ping, "enforcesSecureChat") is True
    assert bot.adapter.calls == [("Server", "get_status", None)]


@pytest.mark.asyncio
async def test_call_api_dispatches_bot_api(app: App, monkeypatch):
    adapter = nonebot.get_adapter(Adapter)
    bot = Bot(adapter, "Server")
    calls = []

    async def fake_send_websocket_message(bot_id, api, data):
        calls.append((bot_id, api, data))
        return "command result"

    monkeypatch.setattr(adapter, "send_websocket_message", fake_send_websocket_message)

    result = await adapter._call_api(bot, "send_rcon_command", command="list")

    assert result == "command result"
    assert calls == [("Server", "send_rcon_command", {"command": "list"})]


@pytest.mark.asyncio
async def test_call_api_dispatches_get_status(app: App, monkeypatch):
    adapter = nonebot.get_adapter(Adapter)
    bot = Bot(adapter, "Server")
    calls = []
    status = STATUS_DATA

    async def fake_send_websocket_message(bot_id, api, data=None):
        calls.append((bot_id, api, data))
        return status

    monkeypatch.setattr(adapter, "send_websocket_message", fake_send_websocket_message)

    result = await adapter._call_api(bot, "get_status")

    assert isinstance(result, Status)
    assert result.timestamp == 1775444822691
    assert result.server_list_ping.players is not None
    assert result.server_list_ping.players.max == 20.0
    assert calls == [("Server", "get_status", None)]


@pytest.mark.asyncio
async def test_call_api_raises_api_not_available(app: App):
    adapter = nonebot.get_adapter(Adapter)
    bot = Bot(adapter, "Server")

    with pytest.raises(ApiNotAvailable):
        await adapter._call_api(bot, "unknown_api")


@pytest.mark.asyncio
async def test_send_websocket_message_requires_connection():
    adapter = nonebot.get_adapter(Adapter)

    with pytest.raises(NetworkError, match="Bot Server is not connected"):
        await adapter.send_websocket_message("Server", "send_msg", {"message": {"text": "hello"}})


@pytest.mark.asyncio
async def test_send_websocket_message_raises_action_failed(app: App):
    adapter = nonebot.get_adapter(Adapter)
    websocket = FakeWebSocket()
    adapter.connections["Server"] = websocket  # type: ignore[assignment]

    async def add_failed_result():
        await asyncio.sleep(0)
        echo = json.loads(websocket.messages[0])["echo"]
        adapter._result_store.add_result(
            {"echo": echo, "status": "FAILED", "message": "bad request", "reason": "invalid"}
        )

    asyncio.create_task(add_failed_result())

    with pytest.raises(ActionFailed) as exc_info:
        await adapter.send_websocket_message("Server", "send_msg", {"message": {"text": "hello"}})

    assert exc_info.value.message == "bad request"
    assert exc_info.value.info["reason"] == "invalid"
    payload = json.loads(websocket.messages[0])
    assert payload == {
        "api": "send_msg",
        "data": {"message": {"text": "hello"}},
        "echo": payload["echo"],
    }
    assert payload["echo"].isdecimal()


@pytest.mark.asyncio
async def test_send_websocket_message_sends_null_data_for_get_status(app: App):
    adapter = nonebot.get_adapter(Adapter)
    websocket = FakeWebSocket()
    adapter.connections["Server"] = websocket  # type: ignore[assignment]
    status = STATUS_DATA

    async def add_status_result():
        await asyncio.sleep(0)
        echo = json.loads(websocket.messages[0])["echo"]
        adapter._result_store.add_result(
            {
                "api": "get_status",
                "code": 200,
                "post_type": "response",
                "status": "SUCCESS",
                "message": "success",
                "data": status,
                "echo": echo,
            }
        )

    asyncio.create_task(add_status_result())

    result = await adapter.send_websocket_message("Server", "get_status", None)

    assert result == status
    payload = json.loads(websocket.messages[0])
    assert payload == {
        "api": "get_status",
        "data": None,
        "echo": payload["echo"],
    }
    assert payload["echo"].isdecimal()


@pytest.mark.asyncio
async def test_send_websocket_message_timeout(monkeypatch):
    adapter = nonebot.get_adapter(Adapter)
    websocket = FakeWebSocket()
    adapter.connections["Server"] = websocket  # type: ignore[assignment]

    async def fake_fetch(self, seq, timeout):
        raise asyncio.TimeoutError

    monkeypatch.setattr(ResultStore, "fetch", fake_fetch)

    with pytest.raises(NetworkError, match="WebSocket call api send_msg timeout"):
        await adapter.send_websocket_message("Server", "send_msg", {"message": {"text": "hello"}})

    payload = json.loads(websocket.messages[0])
    assert payload == {
        "api": "send_msg",
        "data": {"message": {"text": "hello"}},
        "echo": payload["echo"],
    }
    assert payload["echo"].isdecimal()
