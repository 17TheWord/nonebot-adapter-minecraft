from typing import Literal, Optional

from nonebot.typing import overrides
from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent

from ..message import Message


class Event(BaseEvent):
    post_type: str
    event_name: str
    server_name: str
    sub_type: str

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
class BasePlayer(BaseModel):
    # 玩家信息
    nickname: str

    class Config:
        extra = "allow"


# Message Events
class MessageEvent(Event):
    """消息事件"""
    post_type: Literal["message"]
    player: BasePlayer

    def get_message(self) -> Message:
        pass

    def get_plaintext(self) -> str:
        pass

    def get_user_id(self) -> str:
        return self.player.nickname

    def get_session_id(self) -> str:
        return self.player.nickname


class BaseChatEvent(MessageEvent):
    """聊天事件"""
    sub_type: Literal["chat"]
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

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Message from @{self.player.nickname} on [Server:{self.server_name}]: {self.message}"


class BaseDeathEvent(MessageEvent):
    """死亡事件"""
    sub_type: Literal["death"]
    death_message: Optional[Message] = None

    @overrides(Event)
    def get_message(self) -> Message:
        return self.death_message

    def get_plaintext(self) -> str:
        pass

    def get_user_id(self) -> str:
        pass

    def get_session_id(self) -> str:
        pass

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Died on [Server:{self.server_name}]"


class NoticeEvent(Event):
    """通知事件"""
    post_type: Literal["notice"]
    player: BasePlayer

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
        return f"Notice from @{self.player.nickname} on [Server:{self.server_name}]"


class BaseJoinEvent(NoticeEvent):
    """加入事件"""
    sub_type: Literal["join"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Joined [Server:{self.server_name}]"


class BaseQuitEvent(NoticeEvent):
    """玩家离开事件"""
    sub_type: Literal["quit"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Quit [Server:{self.server_name}]"
