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
    """Fabric Player"""

    ip: Optional[str] = None
    display_name: Optional[str] = None
    movement_speed: Optional[float] = None

    block_x: Optional[int] = None
    block_y: Optional[int] = None
    block_z: Optional[int] = None

    is_creative: Optional[bool] = None
    is_spectator: Optional[bool] = None
    is_sneaking: Optional[bool] = None
    is_sleeping: Optional[bool] = None
    is_climbing: Optional[bool] = None
    is_swimming: Optional[bool] = None


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
