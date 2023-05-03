from typing import Literal

from .baseevent import BasePlayer, BaseChatEvent, BaseDeathEvent, BaseJoinEvent, BaseQuitEvent


class ForgePlayer(BasePlayer):
    uuid: str


class ForgeServerChatEvent(BaseChatEvent):
    event_name: Literal["ForgeServerChatEvent"]
    player: ForgePlayer


class ForgePlayerLoggedInEvent(BaseJoinEvent):
    event_name: Literal["ForgePlayerLoggedInEvent"]
    player: ForgePlayer


class ForgePlayerLoggedOutEvent(BaseQuitEvent):
    event_name: Literal["ForgePlayerLoggedOutEvent"]
    player: ForgePlayer
