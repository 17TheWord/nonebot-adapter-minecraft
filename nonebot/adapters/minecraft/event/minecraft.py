from typing import Literal

from .base import BasePlayer, BaseChatEvent, BaseJoinEvent, BaseQuitEvent


class Player(BasePlayer):
    """原版 Player"""


class PlayerChatEvent(BaseChatEvent):
    """原版 玩家聊天事件"""

    event_name: Literal["MinecraftPlayerChatEvent"]
    player: Player


class PlayerJoinEvent(BaseJoinEvent):
    """原版 玩家加入事件"""

    event_name: Literal["MinecraftPlayerJoinEvent"]
    player: Player


class PlayerQuitEvent(BaseQuitEvent):
    """原版 玩家退出事件"""

    event_name: Literal["MinecraftPlayerQuitEvent"]
    player: Player
