from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

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

    text: str | None = None
    color: TextColor | str | None = None
    font: FontEnum | str | None = None
    bold: bool | None = None
    italic: bool | None = None
    underlined: bool | None = None
    strikethrough: bool | None = None
    obfuscated: bool | None = None
    insertion: str | dict[str, Any] | None = None

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

    action: ClickAction | str | None = None
    value: str | None = None


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

    id: str | None = None
    """Spigot, Forge, Fabric"""
    count: int | None = None
    """Spigot, Forge, Fabric"""
    tag: str | None = None
    """Spigot"""
    key: str | None = None
    """Velocity"""


class HoverEntity(BaseModel):
    """
    悬停事件中的实体
    """

    type: str | None = None
    """Spigot, Forge, Fabric"""
    id: str | None = None
    """Spigot"""
    name: list[BaseComponent] | None = None
    """Spigot, Forge, Fabric"""
    key: str | None = None
    """Velocity"""


class HoverEvent(BaseModel):
    """
    悬停事件，传参请传action 和 text/item/entity (三选一)
    """

    action: HoverAction | str | None = None
    text: list[BaseComponent] | None = None
    item: HoverItem | None = None
    entity: HoverEntity | None = None


class TextComponent(BaseComponent):
    """
    TextComponent
    """

    click_event: ClickEvent | None = None
    hover_event: HoverEvent | None = None


class ChatImageModComponent(BaseModel):
    """
    ChatImage Mod 图片
    """

    url: str | None = None
    name: str | None = "图片"

    def __str__(self):
        return f"[[CICode,url={self.url},name={self.name}]]"


class TitleItem(BaseModel):
    """
    SendTitle 消息体
    """

    title: list[BaseComponent] | None = None
    subtitle: list[BaseComponent] | None = None
    fadein: int | None = None
    stay: int | None = None
    fadeout: int | None = None


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

    action: HoverAction | None = None
    contents: list[BaseComponent] | str | dict[str, Any] | None = None


class RconStyleComponent(BaseModel):
    """
    Rcon BaseComponent
    """

    color: TextColor | str | None = None
    font: FontEnum | str | None = None
    bold: bool | None = None
    italic: bool | None = None
    underlined: bool | None = None
    strikethrough: bool | None = None
    obfuscated: bool | None = None
    insertion: str | None = None


class RconRichComponent(BaseModel):
    """
    Rcon Text Component
    """

    click_event: RconClickEvent | None = None
    hover_event: RconHoverEvent | None = None


class RconTextComponent(RconStyleComponent):
    """
    Rcon Text Component
    """

    text: str | None = None


class RconRichTextComponent(RconTextComponent, RconRichComponent):
    """
    Rcon Rich Text Component
    """


class RconSelectorComponent(RconStyleComponent):
    """
    Rcon Selector Component
    """

    selector: str | None = None


class RconRichSelectorComponent(RconSelectorComponent, RconRichComponent):
    """
    Rcon Rich Selector Component
    """


class RconScoreboardObjective(BaseModel):
    """
    Rcon Scoreboard Objective
    """

    name: str | None = None
    objective: str | None = None


class RconScoreboardComponent(RconStyleComponent):
    """
    Rcon Scoreboard Component
    """

    score: RconScoreboardObjective | None = None


class RconRichScoreboardComponent(RconScoreboardComponent, RconRichComponent):
    """
    Rcon Rich Scoreboard Component
    """


class RconNBTComponent(RconStyleComponent):
    """
    Rcon NBT Component
    """

    nbt: str | None = None
    interpret: bool | None = None


class RconNBTStorageComponent(RconNBTComponent):
    """
    Rcon NBT Component
    """

    storage: str | None = None


class RconNBTEntityComponent(RconNBTComponent):
    """
    Rcon NBT Component
    """

    entity: str | None = None


class RconNBTBlockComponent(RconNBTComponent):
    """
    Rcon NBT Component
    """

    block: str | None = None


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

    keybind: str | None = None


class RconRichKeybindComponent(RconKeybindComponent, RconRichComponent):
    """
    Rcon Rich Keybind Component
    """


class RconTranslateComponent(RconStyleComponent):
    """
    Rcon Translate Component
    """

    translate: str | None = None
    with_: (
        list[
            RconRichTextComponent
            | RconRichSelectorComponent
            | RconRichScoreboardComponent
            | RconRichNBTStorageComponent
            | RconRichNBTEntityComponent
            | RconRichNBTBlockComponent
            | RconRichKeybindComponent
        ]
        | None
    ) = Field(alias="with")


class RconRichTranslateComponent(RconTranslateComponent, RconRichComponent):
    """
    Rcon Rich Translate Component
    """
