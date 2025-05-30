"""Minecraft 权限辅助。

FrontMatter:
    sidebar_position: 6
    description: minecraft.permission 模块
"""

from typing import Union

from nonebot.permission import Permission

from .event import NoticeEvent, MessageEvent


async def _is_op(event: Union[MessageEvent, NoticeEvent]) -> bool:
    return bool(event.player.is_op)


OP: Permission = Permission(_is_op)
