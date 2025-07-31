from nonebot import get_adapter
from nonebot.adapters.minecraft import Adapter  # type: ignore
from nonebot.adapters.minecraft.config import Server  # type: ignore


def test_config():
    adapter = get_adapter(Adapter)
    config = adapter.minecraft_config  # type: ignore

    assert config.minecraft_server_rcon == {
        "Server": Server(enable_rcon=False, rcon_port=25575, rcon_password="password")
    }
