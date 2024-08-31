from enum import Enum
from typing import Any, Dict, List, Union, Optional

from pydantic import Field, BaseModel
from nonebot.compat import PYDANTIC_V2

"""
Protocol
"""


class TextColor(str, Enum):
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


class FontEnum(str, Enum):
    """
    字体枚举
    """

    DEFAULT = "minecraft:default"

    # TODO Add more fonts


class BaseComponent(BaseModel):
    """
    BaseComponent
    """

    text: Optional[str] = None
    color: Optional[Union[TextColor, str]] = None
    font: Optional[Union[FontEnum, str]] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underlined: Optional[bool] = None
    strikethrough: Optional[bool] = None
    obfuscated: Optional[bool] = None
    insertion: Optional[Union[str, Dict[str, Any]]] = None

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


class ClickAction(str, Enum):
    """
    点击事件枚举
    """

    OPEN_URL = "open_url"
    OPEN_FILE = "open_file"
    RUN_COMMAND = "run_command"
    SUGGEST_COMMAND = "suggest_command"
    CHANGE_PAGE = "change_page"  # 仅用于书翻页
    COPY_TO_CLIPBOARD = "copy_to_clipboard"


class ClickEvent(BaseModel):
    """
    点击事件
    """

    action: Optional[Union[ClickAction, str]] = None
    value: Optional[str] = None


class HoverAction(str, Enum):
    """
    悬停事件枚举
    """

    SHOW_TEXT = "show_text"
    SHOW_ITEM = "show_item"
    SHOW_ENTITY = "show_entity"


class HoverItem(BaseModel):
    """
    悬停事件中的物品
    """

    id: Optional[str] = None
    """Spigot, Forge, Fabric"""
    count: Optional[int] = None
    """Spigot, Forge, Fabric"""
    tag: Optional[str] = None
    """Spigot"""
    key: Optional[str] = None
    """Velocity"""


class HoverEntity(BaseModel):
    """
    悬停事件中的实体
    """

    type: Optional[str] = None
    """Spigot, Forge, Fabric"""
    id: Optional[str] = None
    """Spigot"""
    name: Optional[List[BaseComponent]] = None
    """Spigot, Forge, Fabric"""
    key: Optional[str] = None
    """Velocity"""


class HoverEvent(BaseModel):
    """
    悬停事件，传参请传action 和 text/item/entity (三选一)
    """

    action: Optional[Union[HoverAction, str]] = None
    text: Optional[List[BaseComponent]] = None
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


class TitleItem(BaseModel):
    """
    SendTitle 消息体
    """

    title: Optional[List[BaseComponent]] = None
    subtitle: Optional[List[BaseComponent]] = None
    fadein: Optional[int] = None
    stay: Optional[int] = None
    fadeout: Optional[int] = None


"""
Rcon
"""


class RconFontEnum(str, Enum):
    """
    Rcon FontEnum
    """

    DEFAULT = "minecraft:default"


class RconClickEvent(ClickEvent):
    """
    Rcon ClickEvent
    """


class RconHoverEvent(BaseModel):
    """
    悬停事件
    """

    action: Optional[HoverAction] = None
    contents: Optional[Union[List[BaseComponent], str, Dict[str, Any]]] = None


class RconStyleComponent(BaseModel):
    """
    Rcon BaseComponent
    """

    color: Optional[Union[TextColor, str]] = None
    font: Optional[Union[FontEnum, str]] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underlined: Optional[bool] = None
    strikethrough: Optional[bool] = None
    obfuscated: Optional[bool] = None
    insertion: Optional[str] = None


class RconRichComponent(BaseModel):
    """
    Rcon Text Component
    """

    click_event: Optional[RconClickEvent] = None
    hover_event: Optional[RconHoverEvent] = None


class RconTextComponent(RconStyleComponent):
    """
    Rcon Text Component
    """

    text: Optional[str] = None


class RconRichTextComponent(RconTextComponent, RconRichComponent):
    """
    Rcon Rich Text Component
    """


class RconSelectorComponent(RconStyleComponent):
    """
    Rcon Selector Component
    """

    selector: Optional[str] = None


class RconRichSelectorComponent(RconSelectorComponent, RconRichComponent):
    """
    Rcon Rich Selector Component
    """


class RconScoreboardObjective(BaseModel):
    """
    Rcon Scoreboard Objective
    """

    name: Optional[str] = None
    objective: Optional[str] = None


class RconScoreboardComponent(RconStyleComponent):
    """
    Rcon Scoreboard Component
    """

    score: Optional[RconScoreboardObjective] = None


class RconRichScoreboardComponent(RconScoreboardComponent, RconRichComponent):
    """
    Rcon Rich Scoreboard Component
    """


class RconNBTComponent(RconStyleComponent):
    """
    Rcon NBT Component
    """

    nbt: Optional[str] = None
    interpret: Optional[bool] = None


class RconNBTStorageComponent(RconNBTComponent):
    """
    Rcon NBT Component
    """

    storage: Optional[str] = None


class RconNBTEntityComponent(RconNBTComponent):
    """
    Rcon NBT Component
    """

    entity: Optional[str] = None


class RconNBTBlockComponent(RconNBTComponent):
    """
    Rcon NBT Component
    """

    block: Optional[str] = None


class RconRichNBTStorageComponent(RconNBTStorageComponent, RconRichComponent):
    """
    Rcon Rich NBT Component
    """


class RconRichNBTEntityComponent(RconNBTEntityComponent, RconRichComponent):
    """
    Rcon Rich NBT Component
    """


class RconRichNBTBlockComponent(RconNBTBlockComponent, RconRichComponent):
    """
    Rcon Rich NBT Component
    """


class RconKeybindComponent(RconStyleComponent):
    """
    Rcon Keybind Component
    """

    keybind: Optional[str] = None


class RconRichKeybindComponent(RconKeybindComponent, RconRichComponent):
    """
    Rcon Rich Keybind Component
    """


class RconTranslateComponent(RconStyleComponent):
    """
    Rcon Translate Component
    """

    translate: Optional[str] = None
    with_: Optional[List[Union[
        RconRichTextComponent, RconRichSelectorComponent, RconRichScoreboardComponent,
        RconRichNBTStorageComponent, RconRichNBTEntityComponent, RconRichNBTBlockComponent,
        RconRichKeybindComponent
    ]]] = Field(alias="with")


class RconRichTranslateComponent(RconTranslateComponent, RconRichComponent):
    """
    Rcon Rich Translate Component
    """
