from aiomcrcon.errors import ClientNotConnectedError as BaseClientNotConnectedError
from aiomcrcon.errors import IncorrectPasswordError as BaseIncorrectPasswordError
from aiomcrcon.errors import RCONConnectionError as BaseRCONConnectionError

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
    def __init__(self, response: Response):
        self.status_code: int = response.status_code
        self.code: int | None = None
        self.message: str | None = None
        self.data: dict | None = None


class RCONConnectionError(NetworkError, BaseRCONConnectionError):
    def __init__(self, msg: str | None = None, error: Exception | None = None):
        self.msg = msg
        self.message = msg
        self.error = error


class IncorrectPasswordError(NetworkError, BaseIncorrectPasswordError):
    def __init__(self):
        super().__init__()
        self.msg = "The password provided to the client was incorrect according to the server."


class ClientNotConnectedError(NetworkError, BaseClientNotConnectedError):
    def __init__(self):
        super().__init__()
        self.msg = "The client isn't connected. (Looks like you forgot to call the connect() coroutine!)"


class UnauthorizedException(ActionFailed):
    pass


class RateLimitException(ActionFailed):
    pass


class ApiNotAvailable(BaseApiNotAvailable, MinecraftAdapterException):
    pass
