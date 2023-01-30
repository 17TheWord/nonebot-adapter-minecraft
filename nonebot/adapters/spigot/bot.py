from typing import Union, Any, TYPE_CHECKING

from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event
from nonebot.typing import overrides

from .utils import get_connections
from .event import Event
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.internal.adapter import Adapter


class Bot(BaseBot):
    @overrides(BaseBot)
    def __init__(self, adapter: "Adapter", self_name: str):
        self.adapter: "Adapter" = adapter
        """协议适配器实例"""
        self.self_id: str = self_name
        """机器人 ID"""

    @overrides(BaseBot)
    async def send(
            self,
            event: Event,
            message: Union[str, Message, MessageSegment],
            **kwargs,
    ) -> Any:
        await get_connections[event.server_name].send_text(data=message)

    async def handle_event(self, event: Event) -> None:
        """处理收到的事件。"""
        await handle_event(self, event)
