from typing import Literal, Optional

from .base import (
    BasePlayer,
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BasePlayerCommandEvent,
)


class Player(BasePlayer):
    """Velocity Player"""

    ping: Optional[int] = None
    online_mode: Optional[bool] = None
    game_profile: Optional[dict] = None
    remote_address: Optional[str] = None
    player_settings: Optional[dict] = None

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
