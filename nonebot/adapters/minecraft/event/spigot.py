from typing import Literal

from mcqq_tool.event.spigot import Player

from .base import (
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BaseDeathEvent,
    BasePlayerCommandEvent
)


class AsyncPlayerChatEvent(BaseChatEvent):
    """聊天事件"""
    event_name: Literal["AsyncPlayerChatEvent"]
    player: Player


class PlayerCommandPreprocessEvent(BasePlayerCommandEvent):
    """玩家命令事件"""
    event_name: Literal["PlayerCommandPreprocessEvent"]
    player: Player


class PlayerDeathEvent(BaseDeathEvent):
    """玩家死亡事件"""
    event_name: Literal["PlayerDeathEvent"]
    player: Player


class PlayerJoinEvent(BaseJoinEvent):
    """玩家加入事件"""
    event_name: Literal["PlayerJoinEvent"]
    player: Player


class PlayerQuitEvent(BaseQuitEvent):
    """玩家离开事件"""
    event_name: Literal["PlayerQuitEvent"]
    player: Player
