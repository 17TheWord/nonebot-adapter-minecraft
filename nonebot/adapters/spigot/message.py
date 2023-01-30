from typing import Iterable, Optional, Type

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment
from nonebot.internal.adapter.message import TMS
from nonebot.typing import overrides


class MessageSegment(BaseMessageSegment):

    def __str__(self) -> str:
        return self.data["message"]

    def __add__(self, other) -> "Message":
        return Message(self) + other

    def __radd__(self, other) -> "Message":
        return Message(other) + self

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        """当前消息段是否为纯文本"""
        return True

    @staticmethod
    def text(msg: str):
        return MessageSegment("text", {"message": msg})


class Message(BaseMessage):

    @classmethod
    def get_segment_class(cls) -> Type[TMS]:
        pass

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: Optional[str] = None) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
