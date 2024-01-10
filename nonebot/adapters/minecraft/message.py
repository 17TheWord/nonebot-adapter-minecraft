from typing import Iterable, Optional, Type

from nonebot.adapters import (
    Message as BaseMessage,
    MessageSegment as BaseMessageSegment,
)
from nonebot.typing import overrides

from .model import (
    TextColor,
    ClickEvent,
    HoverEvent,
    TextComponent,
    ActionBarComponent,
    BaseComponent,
    ChatImageModComponent,
    SendTitleItem,
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
            color: Optional[TextColor] = TextColor.WHITE,
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
            color=color.value,  # todo fix
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

        return MessageSegment("text", text_component.dict())

    @staticmethod
    def title(
            title: str,
            subtitle: Optional[str] = None,
            fadein: Optional[int] = 10,
            stay: Optional[int] = 70,
            fadeout: Optional[int] = 20,
    ):
        title_component = SendTitleItem(
            title=title, subtitle=subtitle, fadein=fadein, stay=stay, fadeout=fadeout
        )

        return MessageSegment("title", title_component.dict())

    @staticmethod
    def actionbar(
            text: Optional[str] = None,
            color: Optional[TextColor] = TextColor.WHITE,
            font: Optional[str] = None,
            bold: Optional[bool] = False,
            italic: Optional[bool] = False,
            underlined: Optional[bool] = False,
            strikethrough: Optional[bool] = False,
            obfuscated: Optional[bool] = False,
            insertion: Optional[str] = None,
    ):
        actionbar_component = ActionBarComponent(
            text=text,
            color=color.value,
            font=font,
            bold=bold,
            italic=italic,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            insertion=insertion,
        )
        return MessageSegment("actionbar", actionbar_component.dict())

    @staticmethod
    def chat_image_mod(
            url: str,
            name: Optional[str] = "图片",
            color: Optional[TextColor] = TextColor.WHITE,
            font: Optional[str] = None,
            bold: Optional[bool] = False,
            italic: Optional[bool] = False,
            underlined: Optional[bool] = False,
            strikethrough: Optional[bool] = False,
            obfuscated: Optional[bool] = False,
            insertion: Optional[str] = None,
    ):
        chat_image_model = ChatImageModComponent(url=url, name=name)

        base_component = BaseComponent(
            text=str(chat_image_model),
            color=color,
            font=font,
            bold=bold,
            italic=italic,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            insertion=insertion,
        )
        return MessageSegment("chat_image_mod", base_component.dict())


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: Optional[str] = None) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
