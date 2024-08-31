from uuid import UUID
from typing import Any, Dict, Union, Optional

from pydantic import BaseModel
from nonebot.compat import PYDANTIC_V2
from nonebot.utils import logger_wrapper
from nonebot.utils import DataclassEncoder as BaseDataclassEncoder

from .exception import ActionFailed

log = logger_wrapper("Minecraft")


class DataclassEncoder(BaseDataclassEncoder):
    """继承并扩展 DataclassEncoder，添加对 UUID 的处理"""

    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)


def zip_dict(data: Union[BaseModel, Dict[str, Any]]) -> Dict[str, Any]:
    """
    将字典中的空值去除
    :param data: 字典数据
    :return: 处理后的字典数据
    """
    temp_dict = {}
    if isinstance(data, BaseModel):
        data = data.model_dump() if PYDANTIC_V2 else data.dict()
    else:
        data = data.copy()
    for k, v in data.items():
        if v:
            if isinstance(v, dict):
                temp_dict[k] = zip_dict(v)
            elif isinstance(v, list):
                temp_dict[k] = [zip_dict(i) for i in v]
            else:
                temp_dict[k] = v
    return temp_dict


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
