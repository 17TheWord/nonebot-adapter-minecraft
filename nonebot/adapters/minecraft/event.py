from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from nonebot.adapters import Event as BaseEvent
from nonebot.compat import PYDANTIC_V2, ConfigDict, model_dump
from nonebot.typing import overrides
from nonebot.utils import escape_tag

from .message import Message


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
        model_config = ConfigDict(extra="allow")  # type: ignore
    else:

        class Config(ConfigDict):
            extra = "allow"


# Models
class Player(BaseModel):
    """玩家信息"""

    nickname: str
    """玩家昵称"""
    uuid: UUID | None = None
    """玩家UUID"""
    is_op: bool | None = None
    """玩家是否为管理员"""
    address: str | None = None
    """玩家IP地址"""

    health: float | None = None
    """玩家当前生命值"""
    max_health: float | None = None
    """玩家最大生命值"""

    experience_level: int | None = None
    """玩家经验等级"""
    experience_progress: float | None = None
    """当前经验进度，0.0-1.0 之间的浮点数"""
    total_experience: int | None = None
    """玩家总经验值"""

    walk_speed: float | None = None
    """玩家行走速度"""

    x: float | None = None
    """玩家坐标X轴"""
    y: float | None = None
    """玩家坐标Y轴"""
    z: float | None = None
    """玩家坐标Z轴"""

    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")  # type: ignore
    else:

        class Config(ConfigDict):
            extra = "allow"


# Message Events
class MessageEvent(Event):
    """消息事件"""

    message_id: str | None = ""
    to_me: bool | None = False
    raw_message: str | None = None
    post_type: Literal["message"]
    player: Player

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.player.nickname

    @overrides(Event)
    def get_session_id(self) -> str:
        return self.player.nickname


class PlayerChatEvent(MessageEvent):
    """玩家聊天事件"""

    event_name: Literal["PlayerChatEvent"]
    sub_type: Literal["player_chat"]
    message: Message

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Message from @{self.player.nickname} on [{self.server_name}]: {self.message}"


class PlayerCommandEvent(MessageEvent):
    """玩家命令事件"""

    event_name: Literal["PlayerCommandEvent"]
    sub_type: Literal["player_command"]
    command: str

    @overrides(Event)
    def get_message(self) -> Message:
        return Message(self.command)

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Command from @{self.player.nickname} on [{self.server_name}]: {self.command}"


class NoticeEvent(Event):
    """通知事件"""

    post_type: Literal["notice"]
    player: Player

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Notice from @{self.player.nickname} on [{self.server_name}]"


class PlayerJoinEvent(NoticeEvent):
    """加入事件"""

    event_name: Literal["PlayerJoinEvent"]
    sub_type: Literal["player_join"]

    @overrides(NoticeEvent)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Joined [{self.server_name}]"


class PlayerQuitEvent(NoticeEvent):
    """玩家离开事件"""

    event_name: Literal["PlayerQuitEvent"]
    sub_type: Literal["player_quit"]

    @overrides(NoticeEvent)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Quit [{self.server_name}]"


class DeathModel(BaseModel):
    """死亡信息模型"""

    key: str | None = None
    """死亡消息的关键字"""

    args: list[str] | None = None
    """死亡消息的参数列表"""

    text: str | None = None
    """死亡消息内容"""


class PlayerDeathEvent(NoticeEvent):
    """玩家死亡事件"""

    event_name: Literal["PlayerDeathEvent"]
    sub_type: Literal["player_death"]
    death: DeathModel

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Died on [{self.server_name}]: {self.death.text if self.death.text else f'{self.player.nickname} died'}"


class DisplayModel(BaseModel):
    """成就显示信息模型"""

    title: str | None = None
    """显示标题"""

    description: str | None = None
    """显示描述"""

    frame: str | None = None
    """显示框架类型"""


class AchievementModel(BaseModel):
    """成就信息模型"""

    display: DisplayModel | None = None
    """成就显示信息"""

    text: str | None = None
    """成就文本描述"""


class PlayerAchievementEvent(NoticeEvent):
    """玩家成就事件"""

    event_name: Literal["PlayerAchievementEvent"]
    sub_type: Literal["player_achievement"]
    achievement: AchievementModel

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"@{self.player.nickname} Achievement on [{self.server_name}]: {self.achievement.text if self.achievement.text else f'{self.player.nickname} has earned an achievement'}"
