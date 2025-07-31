from typing import Any
from uuid import UUID

from aiomcrcon import Client

from nonebot.adapters import Bot as BaseBot
from nonebot.internal.adapter import Adapter

from .event import Event, MessageEvent
from .message import Message, MessageSegment

def _check_nickname(bot: Bot, event: MessageEvent): ...
async def send(bot: Bot, event: Event, message: str | Message | MessageSegment, **kwargs) -> Any: ...

class Bot(BaseBot):
    rcon: Client | None

    def __init__(self, adapter: Adapter, self_id: str, rcon: Client | None = None) -> None: ...
    async def call_api(self, api: str, **data: Any) -> Any: ...
    async def handle_event(self, event: Event) -> None: ...
    async def send(self, event: Event, message: str | Message | MessageSegment, **kwargs) -> Any: ...
    async def send_private_msg(
        self,
        uuid: UUID | None = None,
        nickname: str | None = None,
        message: str | Message | MessageSegment | None = None,
        **kwargs,
    ) -> Any: ...
    async def send_msg(self, message: str | Message | MessageSegment) -> Any: ...
    async def broadcast(self, message: str | Message | MessageSegment) -> Any: ...
    async def send_actionbar(self, message: str | Message | MessageSegment, **kwargs) -> Any: ...
    async def send_title(
        self,
        title: str | Message | MessageSegment,
        subtitle: str | Message | MessageSegment | None = None,
        fadein: int | None = 10,
        stay: int | None = 70,
        fadeout: int | None = 20,
        **kwargs,
    ) -> Any: ...
    async def send_rcon_cmd(self, command: str) -> tuple[str, int]: ...
