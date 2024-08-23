from uuid import UUID
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

from .base import (
    BasePlayer,
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BasePlayerCommandEvent,
)


class GameProfile(BaseModel):
    """Velocity GameProfile"""

    id: Optional[UUID] = None
    undashedId: Optional[UUID] = None
    name: Optional[str] = None
    properties: Optional[List[Any]] = None


class Settings(BaseModel):
    """Velocity Settings"""

    locale: Optional[str] = None
    viewDistance: Optional[int] = None
    chatVisibility: Optional[int] = None
    chatColors: Optional[bool] = None
    difficulty: Optional[int] = None
    skinParts: Optional[int] = None
    mainHand: Optional[int] = None
    chatFilteringEnabled: Optional[bool] = None
    clientListingAllowed: Optional[bool] = None


class Parts(BaseModel):
    """Velocity Parts"""

    bitmask: Optional[int] = None


class PlayerSettings(BaseModel):
    """Velocity Player Settings"""

    settings: Optional[Settings] = None
    parts: Optional[Parts] = None
    locale: Optional[str] = None


class Player(BasePlayer):
    """Velocity Player"""

    ping: Optional[int] = None
    online_mode: Optional[bool] = None
    game_profile: Optional[GameProfile] = None
    remote_address: Optional[Dict[str, Any]] = None
    player_settings: Optional[PlayerSettings] = None


class PlayerChatEvent(BaseChatEvent):
    """Velocity Player Chat Event"""

    event_name: Literal["VelocityPlayerChatEvent"]
    player: Player


class CommandExecuteEvent(BasePlayerCommandEvent):
    """Velocity Command Execute Event"""

    event_name: Literal["VelocityCommandExecuteEvent"]
    player: Player


class LoginEvent(BaseJoinEvent):
    """Velocity Login Event"""

    event_name: Literal["VelocityLoginEvent"]
    player: Player


class DisconnectEvent(BaseQuitEvent):
    """Velocity Disconnect Event"""

    event_name: Literal["VelocityDisconnectEvent"]
    player: Player
