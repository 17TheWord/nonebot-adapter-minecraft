from typing import Union, Any

from nonebot.adapters import Bot as BaseBot
from .event import Event
from .message import Message, MessageSegment


async def send(
        bot: "Bot",
        event: Event,
        message: Union[str, Message, MessageSegment],
) -> Any:
    ...


class Bot(BaseBot):
    async def send(
            self, event: Event, message: Union[str, Message, MessageSegment], **kwargs: Any
    ) -> Any: ...

    async def call_api(self, api: str, **data: Any) -> Any:
        ...

    async def send_msg(self, message: Union[str, Message, MessageSegment]) -> Any:
        ...
