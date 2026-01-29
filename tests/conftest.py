from pathlib import Path

import nonebot
import nonebot.adapters
from nonebug import NONEBOT_INIT_KWARGS
import pytest

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)

from nonebot.adapters.minecraft import Adapter  # type: ignore


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "minecraft_access_token": "test_access_token",
    }


@pytest.fixture(scope="session", autouse=True)
def _init_adapter(nonebug_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)
