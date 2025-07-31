"""NeoForge 事件模型
NeoForge 与 Forge事件名相同，此处协议中的事件名均在前添加 “Neo” 字符以区分
"""

from typing import Literal

from .base import (
    BaseChatEvent,
    BaseDeathEvent,
    BaseJoinEvent,
    BasePlayer,
    BasePlayerCommandEvent,
    BaseQuitEvent,
)


class Player(BasePlayer):
    """NeoForge Player"""

    display_name: str | None = None
    ipAddress: str | None = None

    speed: float | None = None
    flying_speed: float | None = None

    is_flying: bool | None = None
    is_swimming: bool | None = None
    is_sleeping: bool | None = None
    is_blocking: bool | None = None

    game_mode: str | None = None

    block_x: int | None = None
    block_y: int | None = None
    block_z: int | None = None


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
