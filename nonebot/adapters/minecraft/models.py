from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from nonebot.compat import PYDANTIC_V2


class ScoreComponent(BaseModel):
    """计分板文本组件，显示玩家或实体的计分板数值。"""

    name: str
    """计分板条目的名称(通常为玩家名或选择器)。"""

    objective: str
    """计分板目标名称。"""

    value: str | None = None
    """(可选)直接指定显示值，通常仅用于客户端显示。"""


class ClickAction(str, Enum):
    open_url = "open_url"
    open_file = "open_file"
    run_command = "run_command"
    suggest_command = "suggest_command"
    change_page = "change_page"
    copy_to_clipboard = "copy_to_clipboard"


class ClickEvent(BaseModel):
    """点击事件定义，当玩家点击文本时触发的操作。"""

    action: ClickAction | str
    """点击事件类型。"""

    value: str
    """点击事件的参数值，如命令、URL 或页码。"""


class HoverShowItem(BaseModel):
    """鼠标悬停显示物品信息。"""

    id: str
    """物品 ID(例如 "minecraft:diamond_sword")。"""

    count: int | None = None
    """物品数量。"""

    tag: Any | None = None
    """物品的 NBT 数据。"""


class HoverShowEntity(BaseModel):
    """鼠标悬停显示实体信息。"""

    name: "Component | None" = None
    """实体显示名称，可以是文本组件。"""

    type: str | None = None
    """实体类型 ID(例如 "minecraft:zombie")。"""

    id: str | None = None
    """实体的 UUID 字符串。"""


class HoverAction(str, Enum):
    show_text = "show_text"
    show_item = "show_item"
    show_entity = "show_entity"


class HoverEvent(BaseModel):
    """悬停事件定义，当玩家鼠标悬停时显示额外信息。"""

    action: HoverAction | str
    """悬停事件类型。"""

    contents: "Component | str | list[Component] | HoverShowItem | HoverShowEntity | None" = None
    """悬停显示内容，可为文本、物品或实体信息。"""


class Color(str, Enum):
    black = "black"
    dark_blue = "dark_blue"
    dark_green = "dark_green"
    dark_aqua = "dark_aqua"
    dark_red = "dark_red"
    dark_purple = "dark_purple"
    gold = "gold"
    gray = "gray"
    dark_gray = "dark_gray"
    blue = "blue"
    green = "green"
    aqua = "aqua"
    red = "red"
    light_purple = "light_purple"
    yellow = "yellow"
    white = "white"


class Component(BaseModel):
    """Minecraft 聊天文本组件(Chat Component)。"""

    # === 内容字段 ===
    text: str | None = None
    """纯文本内容。最常见的文本组件类型。"""

    translate: str | None = None
    """翻译键(用于多语言文本)，如 "chat.type.text"。"""

    fallback: str | None = None
    """翻译键无效时的备用文本。"""

    with_: "list[str | Component] | None" = Field(default=None, alias="with")
    """用于 `translate` 的参数列表，可为字符串或文本组件。"""

    score: ScoreComponent | None = None
    """计分板组件，用于显示分数。"""

    selector: str | None = None
    """实体选择器(如 "@p")，显示目标名称。"""

    separator: "Component | None" = None
    """当选择器匹配多个实体时的分隔符文本。"""

    keybind: str | None = None
    """键位绑定名称(如 "key.jump")，显示玩家当前键位对应的键名。"""

    nbt: str | None = None
    """NBT 路径表达式，用于读取并显示数据值。"""

    block: str | None = None
    """(可选)NBT 数据来源：方块坐标，如 "1 64 -5"。"""

    entity: str | None = None
    """(可选)NBT 数据来源：实体选择器。"""

    storage: str | None = None
    """(可选)NBT 数据来源：存储命名空间键。"""

    # === 样式属性 ===
    color: Color | str | None = None
    """文本颜色(如 "red"、枚举成员或 "#FF0000")。"""

    font: str | None = None
    """字体资源路径(如 "minecraft:default")。"""

    bold: bool | None = None
    """是否加粗。"""

    italic: bool | None = None
    """是否斜体。"""

    underlined: bool | None = None
    """是否带下划线。"""

    strikethrough: bool | None = None
    """是否带删除线。"""

    obfuscated: bool | None = None
    """是否混淆显示(字符闪烁乱码效果)。"""

    # === 行为属性 ===
    insertion: str | None = None
    """Shift+点击文本时插入到聊天栏的字符串。"""

    click_event: ClickEvent | None = Field(default=None, alias="clickEvent")
    """点击事件定义。"""

    hover_event: HoverEvent | None = Field(default=None, alias="hoverEvent")
    """悬停事件定义。"""

    # === 递归结构 ===
    extra: "list[Component] | None" = None
    """附加的子文本组件，会依次拼接显示。"""

    if PYDANTIC_V2:
        model_config = ConfigDict(populate_by_name=True)
    else:

        class Config:
            allow_population_by_field_name = True


if not PYDANTIC_V2:
    Component.update_forward_refs()
