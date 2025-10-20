from collections.abc import Awaitable, Callable
from functools import partial
from typing import TYPE_CHECKING, Any, Concatenate, Generic, TypeVar, overload
from typing_extensions import ParamSpec
from uuid import UUID

from nonebot.utils import DataclassEncoder as BaseDataclassEncoder
from nonebot.utils import logger_wrapper

from .exception import ActionFailed

log = logger_wrapper("Minecraft")

if TYPE_CHECKING:
    from .bot import Bot

T = TypeVar("T")
TCallable = TypeVar("TCallable", bound=Callable[..., Any])
B = TypeVar("B", bound="Bot")
R = TypeVar("R")
P = ParamSpec("P")


class API(Generic[B, P, R]):
    def __init__(self, func: Callable[Concatenate[B, P], Awaitable[R]]) -> None:
        self.func = func

    def __set_name__(self, owner: type[B], name: str) -> None:
        self.name = name

    @overload
    def __get__(self, obj: None, objtype: type[B]) -> "API[B, P, R]": ...

    @overload
    def __get__(self, obj: B, objtype: type[B] | None) -> Callable[P, Awaitable[R]]: ...

    def __get__(self, obj: B | None, objtype: type[B] | None = None) -> "API[B, P, R] | Callable[P, Awaitable[R]]":
        if obj is None:
            return self

        return partial(obj.call_api, self.name)  # type: ignore

    async def __call__(self, inst: B, *args: P.args, **kwds: P.kwargs) -> R:
        return await self.func(inst, *args, **kwds)


def api(func: TCallable) -> TCallable:
    """装饰器，用于标记 API 方法。

    Args:
        func: 被装饰的函数

    Returns:
        API 实例
    """
    return API(func)  # type: ignore


class DataclassEncoder(BaseDataclassEncoder):
    """继承并扩展 DataclassEncoder，添加对 UUID 的处理"""

    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)


def handle_api_result(result: dict[str, Any] | None) -> Any:
    """处理 API 请求返回值。

    Args:
        result: API 返回数据

    Returns:
        API 调用返回数据

    Raises:
        ActionFailed: API 调用失败
    """
    if isinstance(result, dict):
        if result.get("status") == "FAILED":
            raise ActionFailed(**result)
        return result.get("data")
