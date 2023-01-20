from typing import Optional

from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent

from .message import Message


class Event(BaseEvent):
    event_name: str

    def get_type(self) -> str:
        return self.event_name

    def get_event_name(self) -> str:
        return self.event_name

    def get_event_description(self) -> str:
        return str(self.dict())

    def get_message(self) -> Message:
        raise NotImplementedError

    def get_plaintext(self) -> str:
        raise NotImplementedError

    def get_user_id(self) -> str:
        raise NotImplementedError

    def get_session_id(self) -> str:
        raise NotImplementedError

    def is_tome(self) -> bool:
        return False


# Models
class Player(BaseModel):
    # 玩家信息
    uuid: Optional[str] = None
    nickname: Optional[str] = None
    display_name: Optional[str] = None
    player_list_name: Optional[str] = None
    address: Optional[dict] = None

    class Config:
        extra = "allow"


# Message Events
class MessageEvent(Event):
    """消息事件"""
    server_name: str
    event_name: str
    message: Optional[dict] = None
    player: Player

    def get_message_data(self):
        return self.message["data"]

    def get_message_type(self):
        return self.message["type"]


class AsyncPlayerChatEvent(MessageEvent):
    """聊天事件"""
    server_name: str
    event_name: str
    message: Optional[dict] = None
    player: Player
