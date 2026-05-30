import asyncio
import json
from urllib.parse import quote_plus

import nonebot
from nonebot.adapters.minecraft import (
    Adapter,  # type: ignore
    Bot,
)
from nonebot.drivers import URL
from nonebot.exception import WebSocketClosed
from nonebug import App
import pytest

ORIGINAL_ASYNCIO_SLEEP = asyncio.sleep


class FakeRequest:
    def __init__(self, headers: dict[str, str]):
        self.headers = headers


class FakeWebSocket:
    def __init__(self, headers: dict[str, str], messages: list[str] | None = None):
        self.request = FakeRequest(headers)
        self.messages = messages or []
        self.accepted = False
        self.close_code = None
        self.close_reason = None

    async def accept(self):
        self.accepted = True

    async def receive(self):
        if self.messages:
            return self.messages.pop(0)
        raise WebSocketClosed(1000, "closed")

    async def close(self, code: int = 1000, reason: str | None = None):
        self.close_code = code
        self.close_reason = reason


class FakeWebSocketContext:
    def __init__(self, websocket: FakeWebSocket):
        self.websocket = websocket

    async def __aenter__(self):
        return self.websocket

    async def __aexit__(self, exc_type, exc, tb):
        return False


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


@pytest.mark.asyncio
async def test_ws_server_cleans_connection_after_invalid_json(app: App):
    adapter = nonebot.get_adapter(Adapter)
    headers = {"x-self-name": quote_plus("Server"), "Authorization": "Bearer test_access_token"}
    websocket = FakeWebSocket(headers, ["invalid json"])

    await adapter._handle_ws(websocket)  # type: ignore[arg-type]

    assert websocket.accepted is True
    assert websocket.close_code == 1000
    assert "Server" not in adapter.connections
    assert "Server" not in adapter.bots
    assert "Server" not in nonebot.get_bots()


@pytest.mark.asyncio
async def test_ws_server_stores_response_payload_without_event_task(app: App):
    adapter = nonebot.get_adapter(Adapter)
    headers = {"x-self-name": quote_plus("Server"), "Authorization": "Bearer test_access_token"}
    websocket = FakeWebSocket(
        headers,
        [json.dumps({"post_type": "response", "echo": "1", "status": "OK", "data": "result"})],
    )
    future = asyncio.get_event_loop().create_future()
    adapter._result_store._futures[1] = future

    try:
        await adapter._handle_ws(websocket)  # type: ignore[arg-type]
    finally:
        adapter._result_store._futures.pop(1, None)

    assert future.result() == {"post_type": "response", "echo": "1", "status": "OK", "data": "result"}
    assert websocket.accepted is True
    assert websocket.close_code == 1000
    assert "Server" not in adapter.connections
    assert "Server" not in adapter.bots


@pytest.mark.asyncio
async def test_forward_ws_tracks_event_task(app: App, monkeypatch):
    adapter = nonebot.get_adapter(Adapter)
    headers = {"x-self-name": quote_plus("Server"), "Authorization": "Bearer test_access_token"}
    started = asyncio.Event()
    handled = asyncio.Event()
    release = asyncio.Event()
    websocket = FakeWebSocket(
        headers,
        [
            json.dumps(
                {
                    "timestamp": 0,
                    "post_type": "notice",
                    "event_name": "ServerStartedEvent",
                    "server_name": "Server",
                    "sub_type": "server_started",
                    "server_version": "1.20.1",
                    "server_type": "spigot",
                }
            )
        ],
    )

    def fake_websocket(request):
        return FakeWebSocketContext(websocket)

    async def fake_handle_event(self, event):
        started.set()
        await release.wait()
        handled.set()

    async def fake_receive():
        if websocket.messages:
            return websocket.messages.pop(0)
        await release.wait()
        raise WebSocketClosed(1000, "closed")

    async def stop_after_reconnect(interval):
        raise asyncio.CancelledError

    monkeypatch.setattr(adapter, "websocket", fake_websocket)
    monkeypatch.setattr(Bot, "handle_event", fake_handle_event)
    monkeypatch.setattr(websocket, "receive", fake_receive)
    monkeypatch.setattr(asyncio, "sleep", stop_after_reconnect)

    task = asyncio.create_task(adapter._forward_ws("Server", URL("ws://minecraft/ws")))

    await asyncio.wait_for(started.wait(), timeout=1)
    assert adapter.tasks
    release.set()
    await asyncio.wait_for(handled.wait(), timeout=1)

    with pytest.raises(asyncio.CancelledError):
        await task

    await ORIGINAL_ASYNCIO_SLEEP(0)

    assert adapter.tasks == set()
    assert "Server" not in adapter.connections
    assert "Server" not in adapter.bots
