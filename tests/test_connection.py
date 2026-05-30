import asyncio
from urllib.parse import quote_plus

import nonebot
from nonebot.adapters.minecraft import Adapter  # type: ignore
from nonebug import App
import pytest


class FakeRequest:
    def __init__(self, headers: dict[str, str]):
        self.headers = headers


class FakeWebSocket:
    def __init__(self, headers: dict[str, str]):
        self.request = FakeRequest(headers)
        self.close_code = None
        self.close_reason = None

    async def close(self, code: int = 1000, reason: str | None = None):
        self.close_code = code
        self.close_reason = reason


@pytest.mark.asyncio
async def test_ws_server(app: App):
    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        headers = {"x-self-name": quote_plus("Server"), "Authorization": "Bearer test_access_token"}
        client.headers.update(headers)
        async with client.websocket_connect("/minecraft/ws", headers=headers) as ws:
            await asyncio.sleep(1)
            assert "Server" in nonebot.get_bots()
            assert "Server" in adapter.bots
            await ws.close()

        await asyncio.sleep(1)
        assert "Server" not in nonebot.get_bots()
        assert "Server" not in adapter.bots


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("headers", "reason"),
    [
        ({}, "Missing X-Self-Name Header"),
        (
            {"x-self-name": quote_plus("Server"), "x-client-origin": "nonebot"},
            "X-Client-Origin Header cannot be nonebot",
        ),
        ({"x-self-name": quote_plus("Server")}, "Missing Authorization Header"),
        ({"x-self-name": quote_plus("Server"), "Authorization": "Bearer wrong"}, "Invalid Authorization Header"),
    ],
)
async def test_ws_server_rejects_invalid_handshake(app: App, headers: dict[str, str], reason: str):
    adapter = nonebot.get_adapter(Adapter)
    websocket = FakeWebSocket(headers)

    await adapter._handle_ws(websocket)  # type: ignore[arg-type]

    assert websocket.close_code == 1008
    assert websocket.close_reason == reason
