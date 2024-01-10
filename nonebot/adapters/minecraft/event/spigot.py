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
    """玩家信息"""
    uuid: Optional[str] = None
    display_name: Optional[str] = None
    player_list_name: Optional[str] = None
    is_health_scaled: Optional[bool] = None
    address: Optional[str] = None
    is_sprinting: Optional[bool] = None
    walk_speed: Optional[float] = None
    fly_speed: Optional[float] = None
    is_sneaking: Optional[bool] = None
    level: Optional[int] = None
    is_flying: Optional[bool] = None
    ping: Optional[int] = None
    """Spigot API 1.12.2 Player 无 ping 属性"""
    allow_flight: Optional[bool] = None
    locale: Optional[str] = None
    health_scale: Optional[float] = None
    player_time_offset: Optional[int] = None
    exp: Optional[float] = None
    total_exp: Optional[int] = None
    player_time: Optional[int] = None
    is_player_time_relative: Optional[bool] = None
    is_op: Optional[bool] = None


class AsyncPlayerChatEvent(BaseChatEvent):
    """聊天事件"""
    event_name: Literal["AsyncPlayerChatEvent"]
    player: Player


class PlayerCommandPreprocessEvent(BasePlayerCommandEvent):
    """玩家命令事件"""
    event_name: Literal["PlayerCommandPreprocessEvent"]
    player: Player


class PlayerDeathEvent(BaseDeathEvent):
    """玩家死亡事件"""
    event_name: Literal["PlayerDeathEvent"]
    player: Player


class PlayerJoinEvent(BaseJoinEvent):
    """玩家加入事件"""
    event_name: Literal["PlayerJoinEvent"]
    player: Player


class PlayerQuitEvent(BaseQuitEvent):
    """玩家离开事件"""
    event_name: Literal["PlayerQuitEvent"]
    player: Player
