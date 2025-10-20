from nonebot import get_adapter
from nonebot.adapters.minecraft import Adapter  # type: ignore


def test_config():
    adapter = get_adapter(Adapter)
    config = adapter.minecraft_config  # type: ignore

    assert config.minecraft_access_token == "test_access_token"
