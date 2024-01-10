import re
from typing import Union, Any, TYPE_CHECKING, Callable, Optional

from aiomcrcon import Client
from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event
from nonebot.typing import overrides

from .utils import log
from .event import Event, MessageEvent
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.internal.adapter import Adapter


def _check_nickname(bot: "Bot", event: MessageEvent) -> None:
    """检查消息开头是否存在昵称，去除并赋值 `event.to_me`。

    参数:
        bot: Bot 对象
        event: MessageEvent 对象
    """
    first_msg_seg = event.message[0]
    if first_msg_seg.type != "text":
        return

    nicknames = {re.escape(n) for n in bot.config.nickname}
    if not nicknames:
        return

    # check if the user is calling me with my nickname
    nickname_regex = "|".join(nicknames)
    first_text = first_msg_seg.data["text"]
    if m := re.search(rf"^({nickname_regex})([\s,，]*|$)", first_text, re.IGNORECASE):
        log("DEBUG", f"User is calling me {m[1]}")
        event.to_me = True
        first_msg_seg.data["text"] = first_text[m.end():]


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
    def __init__(
            self, adapter: "Adapter", self_id: str, rcon: Optional[Client] = None
    ):
        self.adapter: "Adapter" = adapter
        """协议适配器实例"""
        self.self_id: str = self_id
        """机器人 ID"""
        self.rcon: Optional[Client] = rcon

    send_handler: Callable[
        ["Bot", Event, Union[str, Message, MessageSegment]], Any
    ] = send

    async def handle_event(self, event: Event) -> None:
        """处理收到的事件。"""
        if isinstance(event, MessageEvent):
            _check_nickname(self, event)

        await handle_event(self, event)

    @overrides(BaseBot)
    async def send(
            self,
            event: Event,
            message: Union[str, Message, MessageSegment],
            **kwargs,
    ) -> Any:
        return await self.__class__.send_handler(self, event, message, **kwargs)
