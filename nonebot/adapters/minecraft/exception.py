from nonebot.drivers import Response
from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import AdapterException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable
from nonebot.exception import NetworkError as BaseNetworkError


class MinecraftAdapterException(AdapterException):
    def __init__(self):
        super().__init__("Minecraft")


class NetworkError(BaseNetworkError, MinecraftAdapterException):
    def __init__(self, msg: str | None = None):
        super().__init__()
        self.msg: str | None = msg
        """错误原因"""

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class ActionFailed(
    BaseActionFailed,
    MinecraftAdapterException,
):
    def __init__(self,**kwargs):
        super().__init__()
        self.info = kwargs
        """所有错误信息"""

    def __repr__(self):
        return "ActionFailed(" + ", ".join(f"{k}={v!r}" for k, v in self.info.items()) + ")"


class UnauthorizedException(ActionFailed):
    pass


class RateLimitException(ActionFailed):
    pass


class ApiNotAvailable(BaseApiNotAvailable, MinecraftAdapterException):
    def __init__(self, msg: str | None = None):
        super().__init__()
        self.msg: str | None = msg
        """错误原因"""
