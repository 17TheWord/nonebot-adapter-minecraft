from typing import Literal, Optional

from pydantic import BaseModel

from .baseevent import BasePlayer, BaseChatEvent, BaseDeathEvent, BaseJoinEvent, BaseQuitEvent


class Address(BaseModel):
    address: str
    port: int


class Player(BasePlayer):
    """玩家信息"""
    uuid: str
    display_name: str
    player_list_name: str
    is_health_scaled: bool
    address: Address
    is_sprinting: bool
    walk_speed: float
    fly_speed: float
    is_sneaking: bool
    level: int
    is_flying: bool
    ping: Optional[int] = None
    """Spigot API 1.12.2 Player 无 ping 属性"""
    allow_flight: bool
    locale: str
    health_scale: float
    player_time_offset: int
    exp: float
    total_exp: int
    player_time: int
    is_player_time_relative: bool


class AsyncPlayerChatEvent(BaseChatEvent):
    """聊天事件"""
    event_name: Literal["AsyncPlayerChatEvent"]
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
