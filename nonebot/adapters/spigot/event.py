from typing import Optional, Literal

from nonebot.typing import overrides
from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent

from .message import Message


class Event(BaseEvent):
    post_type: str
    event_name: str
    server_name: str

    def get_type(self) -> str:
        return self.post_type

    def get_event_name(self) -> str:
        return self.post_type

    def get_message(self) -> "Message":
        raise NotImplementedError

    def get_event_description(self) -> str:
        return str(self.dict())

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
    post_type: Literal["message"]
    player: Player
    message: Message

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    def get_plaintext(self) -> str:
        pass

    def get_user_id(self) -> str:
        pass

    def get_session_id(self) -> str:
        pass


class AsyncPlayerChatEvent(MessageEvent):
    """聊天事件"""
    event_name: Literal["AsyncPlayerChatEvent"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Message from {self.player.nickname}@[Server:{self.server_name}]: {self.message}"


class NoticeEvent(Event):
    """通知事件"""
    post_type: Literal["notice"]
    player: Player

    # message: Message

    def get_message(self) -> Message:
        pass

    def get_plaintext(self) -> str:
        pass

    def get_user_id(self) -> str:
        pass

    def get_session_id(self) -> str:
        pass

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Notice from {self.player.nickname}@[Server:{self.server_name}]"


class PlayerJoinEvent(NoticeEvent):
    """玩家加入事件"""
    event_name: Literal["PlayerJoinEvent"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Notice Join from {self.player.nickname}@[Server:{self.server_name}]: Join"


class PlayerQuitEvent(NoticeEvent):
    """玩家离开事件"""
    event_name: Literal["PlayerQuitEvent"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Notice Quit from {self.player.nickname}@[Server:{self.server_name}]: Quit"


class PlayerDeathEvent(MessageEvent):
    """玩家死亡事件"""
    event_name: Literal["PlayerDeathEvent"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Notice Joined from {self.player.nickname}@[Server:{self.server_name}]: Death"
