from nonebot import get_adapter
from nonebot.adapters.minecraft import Adapter
from nonebot.adapters.minecraft.config import Server


def test_config():
    adapter = get_adapter(Adapter)
    config = adapter.minecraft_config

    assert config.minecraft_server_rcon == {
        "server": Server(enable_rcon=True, rcon_port=25575, rcon_password="password")
    }
