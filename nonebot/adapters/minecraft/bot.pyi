from uuid import UUID
from typing import Any, Tuple, Union, Optional, Callable, TYPE_CHECKING

from nonebot.adapters import Bot as BaseBot
from aiomcrcon import Client

from .event import Event, MessageEvent
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.internal.adapter import Adapter

def _check_nickname(bot: Bot, event: MessageEvent): ...
async def send(
    bot: "Bot", event: Event, message: Union[str, Message, MessageSegment], **kwargs
) -> Any: ...

class Bot(BaseBot):

    def __init__(self, adapter: "Adapter", self_id: str, rcon: Optional[Client] = None) -> None: ...
    async def call_api(self, api: str, **data: Any) -> Any: ...
    async def handle_event(self, event: Event) -> None: ...
    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any: ...
    async def send_private_msg(
        self,
        uuid: Optional[UUID] = None,
        nickname: Optional[str] = None,
        message: Optional[Union[str, Message, MessageSegment]] = None,
        **kwargs,
    ) -> Any: ...
    async def send_msg(self, message: Union[str, Message, MessageSegment]) -> Any: ...
    async def broadcast(self, message: Union[str, Message, MessageSegment]) -> Any: ...
    async def send_actionbar(
        self, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any: ...
    async def send_title(
        self,
        title: Union[str, Message, MessageSegment],
        subtitle: Optional[Union[str, Message, MessageSegment]] = None,
        fadein: Optional[int] = 10,
        stay: Optional[int] = 70,
        fadeout: Optional[int] = 20,
        **kwargs,
    ) -> Any: ...
    async def send_rcon_cmd(self, command: str) -> Tuple[str, int]: ...
