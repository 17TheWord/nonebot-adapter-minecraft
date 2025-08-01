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
    """Folia Player"""

    display_name: str | None = None
    player_list_name: str | None = None
    is_health_scaled: bool | None = None
    address: str | None = None
    is_sprinting: bool | None = None
    walk_speed: float | None = None
    fly_speed: float | None = None
    is_sneaking: bool | None = None
    level: int | None = None
    is_flying: bool | None = None
    ping: int | None = None
    allow_flight: bool | None = None
    locale: str | None = None
    health_scale: float | None = None
    player_time_offset: int | None = None
    exp: float | None = None
    total_exp: int | None = None
    player_time: int | None = None
    is_player_time_relative: bool | None = None
    is_op: bool | None = None


class AsyncPlayerChatEvent(BaseChatEvent):
    """Folia 聊天事件"""

    event_name: Literal["FoliaAsyncPlayerChatEvent"]
    player: Player


class PlayerCommandPreprocessEvent(BasePlayerCommandEvent):
    """Folia 玩家命令事件"""

    event_name: Literal["FoliaPlayerCommandPreprocessEvent"]
    player: Player


class PlayerDeathEvent(BaseDeathEvent):
    """Folia 玩家死亡事件"""

    event_name: Literal["FoliaPlayerDeathEvent"]
    player: Player


class PlayerJoinEvent(BaseJoinEvent):
    """Folia 玩家加入事件"""

    event_name: Literal["FoliaPlayerJoinEvent"]
    player: Player


class PlayerQuitEvent(BaseQuitEvent):
    """Folia 玩家离开事件"""

    event_name: Literal["FoliaPlayerQuitEvent"]
    player: Player
