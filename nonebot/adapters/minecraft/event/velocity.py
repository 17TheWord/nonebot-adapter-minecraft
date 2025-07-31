from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel

from .base import (
    BaseChatEvent,
    BaseJoinEvent,
    BasePlayer,
    BasePlayerCommandEvent,
    BaseQuitEvent,
)


class GameProfile(BaseModel):
    """Velocity GameProfile"""

    id: UUID | None = None
    undashedId: UUID | None = None
    name: str | None = None
    properties: list[Any] | None = None


class Settings(BaseModel):
    """Velocity Settings"""

    locale: str | None = None
    viewDistance: int | None = None
    chatVisibility: int | None = None
    chatColors: bool | None = None
    difficulty: int | None = None
    skinParts: int | None = None
    mainHand: int | None = None
    chatFilteringEnabled: bool | None = None
    clientListingAllowed: bool | None = None


class Parts(BaseModel):
    """Velocity Parts"""

    bitmask: int | None = None


class PlayerSettings(BaseModel):
    """Velocity Player Settings"""

    settings: Settings | None = None
    parts: Parts | None = None
    locale: str | None = None


class Player(BasePlayer):
    """Velocity Player"""

    ping: int | None = None
    online_mode: bool | None = None
    game_profile: GameProfile | None = None
    remote_address: dict[str, Any] | None = None
    player_settings: PlayerSettings | None = None


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
