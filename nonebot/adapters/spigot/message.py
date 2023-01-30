from typing import Iterable, Optional, Type

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment
from nonebot.internal.adapter.message import TMS
from nonebot.typing import overrides


class MessageSegment(BaseMessageSegment):

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    def __str__(self) -> str:
        type_ = self.type
        data = self.data.copy()

        if type_ == "text":
            # return str({"msgType": "text", "msgData": data["msgData"]})
            return data["msgData"]

        params = ",".join(
            [f"{k}={str(v)}" for k, v in data.items() if v is not None]
        )
        return "{msgType=" + f"{type_}{',' if params else ''}{params}" + "}"

    def __add__(self, other) -> "Message":
        return Message(self) + other

    def __radd__(self, other) -> "Message":
        return Message(other) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        """当前消息段是否为纯文本"""
        return True

    @staticmethod
    def text(msg: str):
        return MessageSegment("text", {"msgType": "text", "msgData": msg})

    @staticmethod
    def image(url: str):
        return MessageSegment("image", {"msgType": "image", "msgData": url})

    @staticmethod
    def video(url: str):
        return MessageSegment("video", {"msgType": "video", "msgData": url})


class Message(BaseMessage):

    @classmethod
    def get_segment_class(cls) -> Type[TMS]:
        pass

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: Optional[str] = None) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
