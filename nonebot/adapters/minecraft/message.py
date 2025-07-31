from collections.abc import Iterable

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment
from nonebot.typing import overrides

from .model import (
    ClickEvent,
    HoverEvent,
    TextColor,
    TextComponent,
)


class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> type["Message"]:
        return Message

    def __str__(self) -> str:
        type_ = self.type
        data = self.data.copy()

        if type_ == "text":
            return data["text"]

        params = ",".join([f"{k}={v!s}" for k, v in data.items() if v is not None])
        return "{msg_type=" + f"{type_}{',' if params else ''}{params}" + "}"

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + other

    @overrides(BaseMessageSegment)
    def __radd__(self, other) -> "Message":
        return Message(other) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        """当前消息段是否为纯文本"""
        return True

    @staticmethod
    def text(
        text: str | None = None,
        color: TextColor | None = None,
        font: str | None = None,
        bold: bool | None = False,
        italic: bool | None = False,
        underlined: bool | None = False,
        strikethrough: bool | None = False,
        obfuscated: bool | None = False,
        insertion: str | None = None,
        click_event: ClickEvent | None = None,
        hover_event: HoverEvent | None = None,
    ):
        text_component = TextComponent(
            text=text,
            color=color,
            font=font,
            bold=bold,
            italic=italic,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            insertion=insertion,
            click_event=click_event,
            hover_event=hover_event,
        )

        return MessageSegment("text", text_component.get_dict())


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides
    def get_segment_class(cls) -> type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str | None = None) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
