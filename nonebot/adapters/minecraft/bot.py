from typing import Union, Any, TYPE_CHECKING, Callable, Optional

from aiomcrcon import Client
from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event
from nonebot.typing import overrides

from .event import Event
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.internal.adapter import Adapter


@overrides(BaseBot)
async def send(
        bot: "Bot",
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs,
) -> Any:
    return await bot.send_msg(message=message)


class Bot(BaseBot):
    @overrides(BaseBot)
    def __init__(self, adapter: "Adapter", self_name: str, rcon: Optional[Client] = None):
        self.adapter: "Adapter" = adapter
        """协议适配器实例"""
        self.self_id: str = self_name
        """机器人 ID"""
        self.rcon: Optional[Client] = rcon

    send_handler: Callable[
        ["Bot", Event, Union[str, Message, MessageSegment]], Any
    ] = send

    async def handle_event(self, event: Event) -> None:
        """处理收到的事件。"""
        await handle_event(self, event)

    @overrides(BaseBot)
    async def send(
            self,
            event: Event,
            message: Union[str, Message, MessageSegment],
            **kwargs,
    ) -> Any:
        return await self.__class__.send_handler(self, event, message, **kwargs)
