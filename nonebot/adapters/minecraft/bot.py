from collections.abc import Callable
import re
from typing import TYPE_CHECKING, Any

from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event
from nonebot.typing import overrides

from .event import Event, MessageEvent
from .message import Message, MessageSegment
from .utils import api, log

if TYPE_CHECKING:
    from .adapter import Adapter


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
        first_msg_seg.data["text"] = first_text[m.end() :]


def _parse_message(message):
    if isinstance(message, Message):
        result_msg = message.to_elements()
    elif isinstance(message, MessageSegment):
        result_msg = message.dump()
    else:
        result_msg = MessageSegment.text(text=message).dump()
    return result_msg


@overrides(BaseBot)
async def send(
    bot: "Bot",
    event: Event,
    message: str | Message | MessageSegment,
    **kwargs,
) -> Any:
    return await bot.send_msg(message=message)


class Bot(BaseBot):
    @overrides(BaseBot)
    def __init__(self, adapter: "Adapter", self_id: str):
        super().__init__(adapter, self_id)

    send_handler: Callable[["Bot", Event, str | Message | MessageSegment], Any] = send

    async def handle_event(self, event: Event) -> None:
        """处理收到的事件。"""
        if isinstance(event, MessageEvent):
            _check_nickname(self, event)

        await handle_event(self, event)

    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: str | Message | MessageSegment,
        **kwargs,
    ) -> Any:
        return await self.__class__.send_handler(self, event, message, **kwargs)

    @api
    async def send_msg(
        self,
        message: str | MessageSegment | Message,
    ) -> None:
        """
        发送聊天消息。

        Args:
            message: 要发送的消息内容。
        Returns:
            None
        """
        return await self.adapter.send_websocket_message(self.self_id, "send_msg", {"message": _parse_message(message)})  # type: ignore

    @api
    async def send_title(
        self,
        title: str | MessageSegment | Message | None = None,
        subtitle: str | MessageSegment | Message | None = None,
        fade_in: int = 20,
        stay: int = 70,
        fade_out: int = 20,
    ) -> None:
        """
        发送标题和副标题。

        Args:
            title: 主标题内容。
            subtitle: 副标题内容。
            fade_in: 标题淡入时间(默认20)。
            stay: 标题持续时间(默认70)。
            fade_out: 标题淡出时间(默认20)。
        Returns:
            None
        """
        if not title and not subtitle:
            raise ValueError("At least one of title or subtitle must be provided.")
        data = {
            "title": _parse_message(title) if title else None,
            "subtitle": _parse_message(subtitle) if subtitle else None,
            "fade_in": fade_in,
            "stay": stay,
            "fade_out": fade_out,
        }
        return await self.adapter.send_websocket_message(self.self_id, "send_title", data)  # type: ignore

    @api
    async def send_actionbar(
        self,
        message: str | MessageSegment | Message,
    ) -> None:
        return await self.adapter.send_websocket_message(  # type: ignore
            self.self_id, "send_actionbar", {"message": _parse_message(message)}
        )

    @api
    async def send_rcon_command(
        self,
        command: str,
    ) -> str:
        """
        通过 RCON 发送命令。

        Args:
            command: 要发送的命令字符串。
        Returns:
            命令的执行结果字符串。
        """
        return await self.adapter.send_websocket_message(self.self_id, "send_rcon_command", {"command": command})  # type: ignore
