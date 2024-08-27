from typing import Dict, Any

from nonebot.utils import logger_wrapper

log = logger_wrapper("Minecraft")


def exclude_all_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v}


def exclude_none_and_false(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v not in [None, False]}
