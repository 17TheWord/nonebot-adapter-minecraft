from collections.abc import Iterable

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment
from nonebot.compat import PYDANTIC_V2
from nonebot.typing import overrides

from .models import (
    ClickEvent,
    Color,
    Component,
    HoverEvent,
    ScoreComponent,
)


class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> type["Message"]:
        return Message

    def dump(self) -> dict:
        return self.data

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
        translate: str | None = None,
        fallback: str | None = None,
        with_: list[str | Component] | None = None,
        score: ScoreComponent | None = None,
        selector: str | None = None,
        separator: Component | None = None,
        keybind: str | None = None,
        nbt: str | None = None,
        block: str | None = None,
        entity: str | None = None,
        storage: str | None = None,
        color: Color | str | None = None,
        font: str | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
        underlined: bool | None = None,
        strikethrough: bool | None = None,
        obfuscated: bool | None = None,
        insertion: str | None = None,
        click_event: ClickEvent | None = None,
        hover_event: HoverEvent | None = None,
        extra: list[Component] | None = None,
    ):
        """
        创建一个文本消息段。
        完整文档参考 https://zh.minecraft.wiki/w/%E6%96%87%E6%9C%AC%E7%BB%84%E4%BB%B6

        Args:
            text: 纯文本内容。最常见的文本组件类型。
            translate: 翻译键(用于多语言文本)，如 "chat.type.text"。
            fallback: 翻译键无效时的备用文本。
            with_: 用于 `translate` 的参数列表，可为字符串或文本组件。
            score: 计分板组件，用于显示分数。
            selector: 实体选择器(如 "@p")，显示目标名称。
            separator: 当选择器匹配多个实体时的分隔符文本。
            keybind: 键位绑定名称(如 "key.jump")，显示玩家当前键位对应的键名。
            nbt: NBT 路径表达式，用于读取并显示数据值。
            block: (可选)NBT 数据来源：方块坐标，如 "1 64 -5"。
            entity: (可选)NBT 数据来源：实体选择器。
            storage: (可选)NBT 数据来源：存储命名空间键。
            color: 文本颜色(如 "red"、枚举成员或 "#FF0000")。
            font: 字体资源路径(如 "minecraft:default")。
            bold: 是否加粗。
            italic: 是否斜体。
            underlined: 是否带下划线。
            strikethrough: 是否带删除线。
            obfuscated: 是否混淆显示(字符闪烁乱码效果)。
            insertion: Shift+点击文本时插入到聊天栏的字符串。
            click_event: 点击事件定义。
            hover_event: 悬停事件定义。
            extra: 附加的子文本组件，会依次拼接显示。
        Returns:
            文本消息段实例。
        """
        component = Component(
            text=text,
            translate=translate,
            fallback=fallback,
            # 'with' is a reserved keyword in Python, so we use 'with_'
            score=score,
            selector=selector,
            separator=separator,
            keybind=keybind,
            nbt=nbt,
            block=block,
            entity=entity,
            storage=storage,
            color=color,
            font=font,
            bold=bold,
            italic=italic,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            insertion=insertion,
            clickEvent=click_event,
            hoverEvent=hover_event,
            extra=extra,
        )

        component.with_ = with_

        if PYDANTIC_V2:
            data = component.model_dump(exclude_none=True, by_alias=True)
        else:
            data = component.dict(exclude_none=True, by_alias=True)

        return MessageSegment("text", data)


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides
    def get_segment_class(cls) -> type[MessageSegment]:
        """返回适配器的 MessageSegment 类型本身"""
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str | None = None) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)

    def to_elements(self) -> list[dict]:
        res = []
        for seg in self:
            if isinstance(seg, MessageSegment):
                res.append(seg.dump())
            elif isinstance(seg, str):
                res.append(MessageSegment.text(seg).dump())
        return res
