from enum import Enum
from typing import Any, List, Union, Optional
from pydantic import BaseModel
from nonebot.compat import PYDANTIC_V2

"""
Protocol
"""


class TextColor(Enum):
    """
    颜色枚举
    """

    BLACK = "black"
    DARK_BLUE = "dark_blue"
    DARK_GREEN = "dark_green"
    DARK_AQUA = "dark_aqua"
    DARK_RED = "dark_red"
    DARK_PURPLE = "dark_purple"
    GOLD = "gold"
    GRAY = "gray"
    DARK_GRAY = "dark_gray"
    BLUE = "blue"
    GREEN = "green"
    AQUA = "aqua"
    RED = "red"
    LIGHT_PURPLE = "light_purple"
    YELLOW = "yellow"
    WHITE = "white"

    def __str__(self):
        return self.value


class BaseComponent(BaseModel):
    """
    BaseComponent
    """

    text: Optional[str] = None
    color: Optional[TextColor] = None
    font: Optional[str] = None
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    underlined: Optional[bool] = False
    strikethrough: Optional[bool] = False
    obfuscated: Optional[bool] = False
    insertion: Optional[str] = None

    def __str__(self):
        """
        获取纯文本格式的消息
        :return: 文本消息
        """
        return self.text

    def get_dict(self):
        if PYDANTIC_V2:
            return self.model_dump()
        else:
            return self.dict()


class ClickAction(Enum):
    """
    点击事件枚举
    """

    OPEN_URL = "open_url"
    OPEN_FILE = "open_file"
    RUN_COMMAND = "run_command"
    SUGGEST_COMMAND = "suggest_command"
    CHANGE_PAGE = "change_page"  # 仅用于书翻页
    COPY_TO_CLIPBOARD = "copy_to_clipboard"

    def __str__(self):
        return self.value


class ClickEvent(BaseModel):
    """
    点击事件
    """

    action: Optional[ClickAction] = None
    value: Optional[str] = None


class HoverAction(Enum):
    """
    悬停事件枚举
    """

    SHOW_TEXT = "show_text"
    SHOW_ITEM = "show_item"
    SHOW_ENTITY = "show_entity"

    def __str__(self):
        return self.value


class HoverItem(BaseModel):
    """
    悬停事件中的物品
    """

    id: Optional[Union[str, int]] = None
    count: Optional[int] = None
    tag: Optional[str] = None


class HoverEntity(BaseModel):
    """
    悬停事件中的实体
    """

    type: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None


class HoverEvent(BaseModel):
    """
    悬停事件
    """

    action: Optional[HoverAction] = None
    base_component_list: Optional[List[BaseComponent]] = None
    item: Optional[HoverItem] = None
    entity: Optional[HoverEntity] = None


class TextComponent(BaseComponent):
    """
    TextComponent
    """

    click_event: Optional[ClickEvent] = None
    hover_event: Optional[HoverEvent] = None


class ChatImageModComponent(BaseModel):
    """
    ChatImage Mod 图片
    """

    url: Optional[str] = None
    name: Optional[str] = "图片"

    def __str__(self):
        return f"[[CICode,url={self.url},name={self.name}]]"


class MessageList(BaseModel):
    """
    消息列表
    """

    message_list: Optional[List[TextComponent]] = []


class SendTitleItem(BaseModel):
    """
    SendTitle 消息体
    """

    title: Optional[List[BaseComponent]] = None
    subtitle: Optional[List[BaseComponent]] = None
    fadein: Optional[int] = 10
    stay: Optional[int] = 70
    fadeout: Optional[int] = 20


class SendTitleData(BaseModel):
    """
    SendTitle
    """

    send_title: Optional[SendTitleItem] = None


class SendActionBarData(BaseModel):
    """
    ActionBar 消息体
    """

    message_list: Optional[List[BaseComponent]] = None


class ProtocolData(BaseModel):
    """
    发送的消息体
    """

    api: Optional[str] = None
    data: Optional[Any] = None


"""
Rcon
"""


class RconFontEnum(Enum):
    """
    字体枚举
    """

    DEFAULT = "minecraft:default"

    def __str__(self):
        return self.value


class RconClickEvent(ClickEvent):
    """
    点击事件
    """

    action: Optional[ClickAction] = None
    value: Optional[str] = None


class RconBaseComponent(BaseComponent):
    """
    RconBaseComponent
    """

    score: Optional[dict] = None
    selector: Optional[str] = None
    block: Optional[str] = None
    translate: Optional[str] = None

    def __str__(self):
        """
        获取纯文本格式的消息
        :return: 文本消息
        """
        return self.text

    def get_component(self) -> dict:
        """
        获取组件格式的消息，同时对空值进行过滤
        :return: component
        """
        temp_dict = {}
        for i in self.__dict__:
            if self.__dict__[i]:
                temp_dict[i] = str(self.__dict__[i])
        return temp_dict


class RconHoverEvent(BaseModel):
    """
    悬停事件
    """

    action: Optional[HoverAction] = None
    contents: Optional[List[RconBaseComponent]] = None


class RconTextComponent(RconBaseComponent):
    """
    文本组件
    """

    click_event: Optional[RconClickEvent] = None
    hover_event: Optional[RconHoverEvent] = None


__all__ = [
    "TextColor",
    "HoverItem",
    "ClickEvent",
    "HoverEvent",
    "ClickAction",
    "HoverEntity",
    "MessageList",
    "HoverAction",
    "ProtocolData",
    "RconFontEnum",
    "TextComponent",
    "BaseComponent",
    "SendTitleItem",
    "SendTitleData",
    "RconClickEvent",
    "RconHoverEvent",
    "SendActionBarData",
    "RconBaseComponent",
    "RconTextComponent",
    "ChatImageModComponent",
]
