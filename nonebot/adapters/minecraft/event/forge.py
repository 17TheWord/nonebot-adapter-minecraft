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
    """Forge Player"""

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
    """Forge 聊天事件"""

    event_name: Literal["ServerChatEvent"]
    player: Player


class PlayerLoggedInEvent(BaseJoinEvent):
    """Forge 玩家加入事件"""

    event_name: Literal["PlayerLoggedInEvent"]
    player: Player


class PlayerLoggedOutEvent(BaseQuitEvent):
    """Forge 玩家离开事件"""

    event_name: Literal["PlayerLoggedOutEvent"]
    player: Player


class PlayerDeathEvent(BaseDeathEvent):
    """Forge 玩家死亡事件"""

    event_name: Literal["PlayerDeathEvent"]
    player: Player


class PlayerCommandEvent(BasePlayerCommandEvent):
    """Forge 玩家命令事件"""

    event_name: Literal["CommandEvent"]
    player: Player
