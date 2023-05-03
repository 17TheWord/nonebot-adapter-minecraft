from typing import Literal

from .baseevent import BasePlayer, BasePlayer, BaseChatEvent, BaseJoinEvent, BaseQuitEvent


class MineCraftPlayer(BasePlayer):
    """原版 玩家信息"""


class MinecraftPlayerChatEvent(BaseChatEvent):
    """原版 玩家聊天事件"""
    event_name: Literal["MinecraftPlayerChatEvent"]
    player: MineCraftPlayer


class MinecraftPlayerJoinEvent(BaseJoinEvent):
    """原版 玩家加入事件"""
    event_name: Literal["MinecraftPlayerJoinEvent"]
    player: MineCraftPlayer


class MinecraftPlayerQuitEvent(BaseQuitEvent):
    """原版 玩家退出事件"""
    event_name: Literal["MinecraftPlayerQuitEvent"]
    player: MineCraftPlayer
