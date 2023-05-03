from typing import Literal

from .baseevent import BasePlayer, BaseChatEvent, BaseDeathEvent, BaseJoinEvent, BaseQuitEvent


class Player(BasePlayer):
    uuid: str


class ServerChatEvent(BaseChatEvent):
    event_name: Literal["ForgeServerChatEvent"]
    player: Player


class PlayerLoggedInEvent(BaseJoinEvent):
    event_name: Literal["ForgePlayerLoggedInEvent"]
    player: Player


class PlayerLoggedOutEvent(BaseQuitEvent):
    event_name: Literal["ForgePlayerLoggedOutEvent"]
    player: Player
