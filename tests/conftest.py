from pathlib import Path

from nonebug import NONEBOT_INIT_KWARGS
import pytest

import nonebot
import nonebot.adapters

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)

from nonebot.adapters.minecraft import Adapter  # type: ignore


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "minecraft_server_rcon": {
            "Server": {
                "enable_rcon": False,
                "rcon_port": 25575,
                "rcon_password": "password",
            }
        },
    }


@pytest.fixture(scope="session", autouse=True)
def _init_adapter(nonebug_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)
