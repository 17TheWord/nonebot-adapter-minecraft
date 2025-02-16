from uuid import UUID
from typing import Literal, Optional

from pydantic import BaseModel
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.compat import PYDANTIC_V2, ConfigDict, model_dump

from nonebot.adapters import Event as BaseEvent

from ..message import Message


class Event(BaseEvent):
    """事件基类"""
    timestamp: int
    post_type: str
    event_name: str
    server_name: str
    server_version: str
    server_type: str
    sub_type: str

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.event_name

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(model_dump(self)))

    @overrides(BaseEvent)
    def get_message(self) -> "Message":
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False

    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config(ConfigDict):
            extra = "allow"


# Models
class BasePlayer(BaseModel):
    """玩家基类"""
    nickname: str
    uuid: Optional[UUID] = None
    is_op: Optional[bool] = None

    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:
        class Config(ConfigDict):
            extra = "allow"


# Message Events
class MessageEvent(Event):
    """消息事件"""

    message_id: Optional[str] = ""
    to_me: Optional[bool] = False
    ori_message: Optional[Message] = None
    post_type: Literal["message"]
    player: BasePlayer
    message: Message

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.player.nickname

    @overrides(Event)
    def get_session_id(self) -> str:
        return self.player.nickname


class BaseChatEvent(MessageEvent):
    """聊天事件"""

    sub_type: Literal["chat"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Message from @{self.player.nickname} on [{self.server_name}]: {self.message}"  # noqa: E501


class BasePlayerCommandEvent(MessageEvent):
    """玩家命令事件"""

    sub_type: Literal["player_command"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Command from @{self.player.nickname} on [{self.server_name}]: {self.message}"  # noqa: E501


class BaseDeathEvent(MessageEvent):
    """死亡事件"""

    sub_type: Literal["death"]

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Died on [{self.server_name}]: {self.message}"


class NoticeEvent(Event):
    """通知事件"""

    post_type: Literal["notice"]
    player: BasePlayer

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Notice from @{self.player.nickname} on [{self.server_name}]"


class BaseJoinEvent(NoticeEvent):
    """加入事件"""

    sub_type: Literal["join"]

    @overrides(NoticeEvent)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Joined [{self.server_name}]"


class BaseQuitEvent(NoticeEvent):
    """玩家离开事件"""

    sub_type: Literal["quit"]

    @overrides(NoticeEvent)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Quit [{self.server_name}]"
