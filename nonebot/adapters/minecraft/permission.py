"""Minecraft 权限辅助。

FrontMatter:
    sidebar_position: 6
    description: minecraft.permission 模块
"""

from nonebot.permission import Permission

from .event import MessageEvent, NoticeEvent


async def _is_op(event: MessageEvent | NoticeEvent) -> bool:
    return bool(event.player.is_op)


OP: Permission = Permission(_is_op)
