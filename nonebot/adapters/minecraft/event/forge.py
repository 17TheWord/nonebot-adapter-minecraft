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
    """Forge Player"""

    uuid: Optional[str] = None
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
    """Forge ServerChatEvent"""
    event_name: Literal["ServerChatEvent"]
    player: Player


class PlayerLoggedInEvent(BaseJoinEvent):
    """Forge PlayerLoggedInEvent"""
    event_name: Literal["PlayerLoggedInEvent"]
    player: Player


class PlayerLoggedOutEvent(BaseQuitEvent):
    """Forge PlayerLoggedOutEvent"""
    event_name: Literal["PlayerLoggedOutEvent"]
    player: Player


class PlayerDeathEvent(BaseDeathEvent):
    """Forge PlayerDeathEvent"""
    event_name: Literal["PlayerDeathEvent"]
    player: Player


class PlayerCommandEvent(BasePlayerCommandEvent):
    """Forge CommandEvent"""
    event_name: Literal["CommandEvent"]
    player: Player
