from typing import Type, Iterable, Optional

from nonebot.typing import overrides

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

from .model import (
    TextColor,
    ClickEvent,
    HoverEvent,
    TextComponent,
)


class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    def __str__(self) -> str:
        type_ = self.type
        data = self.data.copy()

        if type_ == "text":
            return data["text"]

        params = ",".join([f"{k}={str(v)}" for k, v in data.items() if v is not None])
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
            text: Optional[str] = None,
            color: Optional[TextColor] = None,
            font: Optional[str] = None,
            bold: Optional[bool] = False,
            italic: Optional[bool] = False,
            underlined: Optional[bool] = False,
            strikethrough: Optional[bool] = False,
            obfuscated: Optional[bool] = False,
            insertion: Optional[str] = None,
            click_event: Optional[ClickEvent] = None,
            hover_event: Optional[HoverEvent] = None,
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
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: Optional[str] = None) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
