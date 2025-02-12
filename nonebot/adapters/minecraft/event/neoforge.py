""" NeoForge 事件模型
NeoForge 与 Forge事件名相同，此处协议中的事件名均在前添加 “Neo” 字符以区分
"""

from typing import Literal, Optional

from .base import (
    BasePlayer,
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BaseDeathEvent,
    BasePlayerCommandEvent,
)


class Player(BasePlayer):
    """NeoForge Player"""

    display_name: Optional[str] = None
    ipAddress: Optional[str] = None

    speed: Optional[float] = None
    flying_speed: Optional[float] = None

    is_flying: Optional[bool] = None
    is_swimming: Optional[bool] = None
    is_sleeping: Optional[bool] = None
    is_blocking: Optional[bool] = None

    game_mode: Optional[str] = None

    block_x: Optional[int] = None
    block_y: Optional[int] = None
    block_z: Optional[int] = None


class ServerChatEvent(BaseChatEvent):
    """NeoForge 聊天事件"""

    event_name: Literal["NeoServerChatEvent"]
    player: Player


class PlayerLoggedInEvent(BaseJoinEvent):
    """NeoForge 玩家加入事件"""

    event_name: Literal["NeoPlayerLoggedInEvent"]
    player: Player


class PlayerLoggedOutEvent(BaseQuitEvent):
    """NeoForge 玩家离开事件"""

    event_name: Literal["NeoPlayerLoggedOutEvent"]
    player: Player


class PlayerDeathEvent(BaseDeathEvent):
    """NeoForge 玩家死亡事件"""

    event_name: Literal["NeoPlayerDeathEvent"]
    player: Player


class PlayerCommandEvent(BasePlayerCommandEvent):
    """NeoForge 玩家命令事件"""

    event_name: Literal["NeoCommandEvent"]
    player: Player
