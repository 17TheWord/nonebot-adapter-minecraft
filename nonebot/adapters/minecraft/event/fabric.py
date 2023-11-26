from typing import Literal

from mcqq_tool.event.fabric import Player

from .base import (
    BaseChatEvent,
    BaseDeathEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BasePlayerCommandEvent
)


class FabricServerMessageEvent(BaseChatEvent):
    """Fabric FabricServerMessageEvent API"""
    event_name: Literal["FabricServerMessageEvent"]
    player: Player


class FabricServerCommandMessageEvent(BasePlayerCommandEvent):
    """Fabric FabricServerCommandMessageEvent API"""
    event_name: Literal["FabricServerCommandMessageEvent"]
    player: Player


class FabricServerLivingEntityAfterDeathEvent(BaseDeathEvent):
    """Fabric FabricServerLivingEntityAfterDeathEvent API"""
    event_name: Literal["FabricServerLivingEntityAfterDeathEvent"]
    player: Player


class FabricServerPlayConnectionJoinEvent(BaseJoinEvent):
    """Fabric FabricServerPlayConnectionJoinEvent API"""
    event_name: Literal["FabricServerPlayConnectionJoinEvent"]
    player: Player


class FabricServerPlayConnectionDisconnectEvent(BaseQuitEvent):
    """Fabric FabricServerPlayConnectionDisconnectEvent API"""
    event_name: Literal["FabricServerPlayConnectionDisconnectEvent"]
    player: Player
