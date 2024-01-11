from typing import Literal, Optional

from .base import (
    BasePlayer,
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BaseDeathEvent,
    BasePlayerCommandEvent
)


class Player(BasePlayer):
    """Forge Player"""
    uuid: Optional[str] = None
    ipAddress: Optional[str] = None
    level: Optional[str] = None
    """地图？"""
    speed: Optional[float] = None


class ServerChatEvent(BaseChatEvent):
    event_name: Literal["ForgeServerChatEvent"]
    player: Player


class PlayerLoggedInEvent(BaseJoinEvent):
    event_name: Literal["ForgePlayerLoggedInEvent"]
    player: Player


class PlayerLoggedOutEvent(BaseQuitEvent):
    event_name: Literal["ForgePlayerLoggedOutEvent"]
    player: Player


class PlayerDeathEvent(BaseDeathEvent):
    event_name: Literal["ForgePlayerDeathEvent"]
    player: Player


class PlayerCommandEvent(BasePlayerCommandEvent):
    event_name: Literal["ForgeCommandEvent"]
    player: Player
