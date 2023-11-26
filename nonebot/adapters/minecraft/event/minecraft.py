from typing import Literal

from mcqq_tool.event.minecraft import Player

from .base import (
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent
)


class MinecraftPlayerChatEvent(BaseChatEvent):
    """原版 玩家聊天事件"""
    event_name: Literal["MinecraftPlayerChatEvent"]
    player: Player


class MinecraftPlayerJoinEvent(BaseJoinEvent):
    """原版 玩家加入事件"""
    event_name: Literal["MinecraftPlayerJoinEvent"]
    player: Player


class MinecraftPlayerQuitEvent(BaseQuitEvent):
    """原版 玩家退出事件"""
    event_name: Literal["MinecraftPlayerQuitEvent"]
    player: Player
