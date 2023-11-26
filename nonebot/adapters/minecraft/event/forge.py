from typing import Literal

from mcqq_tool.event.forge import Player

from .base import (
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BaseDeathEvent
)


class ServerChatEvent(BaseChatEvent):
    event_name: Literal["ForgeServerChatEvent"]
    player: Player


class PlayerLoggedInEvent(BaseJoinEvent):
    event_name: Literal["ForgePlayerLoggedInEvent"]
    player: Player


class PlayerLoggedOutEvent(BaseQuitEvent):
    event_name: Literal["ForgePlayerLoggedOutEvent"]
    player: Player


class ForgePlayerRespawnEvent(BaseDeathEvent):
    event_name: Literal["ForgePlayerRespawnEvent"]
    player: Player
