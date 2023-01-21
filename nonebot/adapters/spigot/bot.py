from typing import Union, Any

from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event
from nonebot.typing import overrides

from .event import Event
from .message import Message, MessageSegment


class Bot(BaseBot):

    @overrides(BaseBot)
    async def send(
            self,
            event: Event,
            message: Union[str, Message, MessageSegment],
            **kwargs,
    ) -> Any:
        print(message)

    async def handle_event(self, event: Event) -> None:
        """处理收到的事件。"""
        await handle_event(self, event)
