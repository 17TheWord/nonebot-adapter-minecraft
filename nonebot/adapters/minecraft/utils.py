from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID
from nonebot.utils import logger_wrapper, DataclassEncoder as BaseDataclassEncoder

from .exception import ActionFailed

log = logger_wrapper("Minecraft")


class DataclassEncoder(BaseDataclassEncoder):
    """继承并扩展 DataclassEncoder，添加对 UUID 的处理"""

    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        elif isinstance(o, Enum):
            return o.value
        return super().default(o)


def handle_api_result(result: Optional[Dict[str, Any]]) -> Any:
    """处理 API 请求返回值。

    参数:
        result: API 返回数据

    返回:
        API 调用返回数据

    异常:
        ActionFailed: API 调用失败
    """
    if isinstance(result, dict):
        if result.get("status") == "FAILED":
            raise ActionFailed(**result)
        return result.get("data")
