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
    """Fabric Player"""

    ip: str | None = None
    display_name: str | None = None
    movement_speed: float | None = None

    block_x: int | None = None
    block_y: int | None = None
    block_z: int | None = None

    is_creative: bool | None = None
    is_spectator: bool | None = None
    is_sneaking: bool | None = None
    is_sleeping: bool | None = None
    is_climbing: bool | None = None
    is_swimming: bool | None = None


class ServerMessageEvent(BaseChatEvent):
    """Fabric 聊天事件"""

    event_name: Literal["ServerMessageEvent"]
    player: Player


class ServerCommandMessageEvent(BasePlayerCommandEvent):
    """Fabric 玩家命令事件"""

    event_name: Literal["ServerCommandMessageEvent"]
    player: Player


class ServerLivingEntityAfterDeathEvent(BaseDeathEvent):
    """ServerLivingEntityAfterDeathEvent API"""

    event_name: Literal["ServerLivingEntityAfterDeathEvent"]
    player: Player


class ServerPlayConnectionJoinEvent(BaseJoinEvent):
    """ServerPlayConnectionJoinEvent API"""

    event_name: Literal["ServerPlayConnectionJoinEvent"]
    player: Player


class ServerPlayConnectionDisconnectEvent(BaseQuitEvent):
    """ServerPlayConnectionDisconnectEvent API"""

    event_name: Literal["ServerPlayConnectionDisconnectEvent"]
    player: Player
