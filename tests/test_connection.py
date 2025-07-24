import asyncio

from nonebug import App
import pytest

import nonebot
from nonebot.adapters.minecraft import Adapter


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoints", ["/minecraft/ws"])
async def test_ws(app: App, endpoints: str):
    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        headers = {"x-self-name": "Server"}
        async with client.websocket_connect(endpoints, headers=headers) as ws:
            assert "Server" in nonebot.get_bots()
            assert "Server" in adapter.bots
            await ws.close()

        await asyncio.sleep(1)
        assert "Server" not in nonebot.get_bots()
        assert "Server" not in adapter.bots
