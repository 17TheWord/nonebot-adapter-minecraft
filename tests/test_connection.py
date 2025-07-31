import asyncio
from urllib.parse import quote_plus

from nonebug import App
import pytest

import nonebot
from nonebot.adapters.minecraft import Adapter  # type: ignore


@pytest.mark.asyncio
async def test_ws_server(app: App):
    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        headers = {"x-self-name": quote_plus("Server")}
        client.headers.update(headers)
        async with client.websocket_connect("/minecraft/ws", headers=headers) as ws:
            await asyncio.sleep(1)
            assert "Server" in nonebot.get_bots()
            assert "Server" in adapter.bots
            await ws.close()

        await asyncio.sleep(1)
        assert "Server" not in nonebot.get_bots()
        assert "Server" not in adapter.bots
