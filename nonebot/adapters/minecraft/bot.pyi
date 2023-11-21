from re import A
from typing import Any, Union

from nonebot.adapters import Bot as BaseBot

from .event import Event, MessageEvent
from .message import Message, MessageSegment

def _check_nickname(bot: Bot, event: MessageEvent): ...
async def send(
    bot: "Bot", event: Event, message: Union[str, Message, MessageSegment], **kwargs
) -> Any: ...

class Bot(BaseBot):
    async def call_api(self, api: str, **data: Any) -> Any: ...
    async def handle_event(self, event: Event) -> None: ...
    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any: ...
    async def send_actionbar(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any: ...
    async def send_title(
        self,
        event: Event,
        title: str,
        message: Union[str, Message, MessageSegment],
        **kwargs,
    ) -> Any: ...
    async def send_msg(
        self,
        message: Union[str, Message, MessageSegment],
    ) -> Any: ...