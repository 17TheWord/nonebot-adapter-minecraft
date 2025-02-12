from .forge import Player as ForgePlayer
from .fabric import Player as FabricPlayer
from .spigot import Player as SpigotPlayer
from .minecraft import Player as MinecraftPlayer
from .velocity import LoginEvent as VelocityLoginEvent
from .forge import ServerChatEvent as ForgeServerChatEvent
from .forge import PlayerDeathEvent as ForgePlayerDeathEvent
from .spigot import PlayerJoinEvent as SpigotPlayerJoinEvent
from .spigot import PlayerQuitEvent as SpigotPlayerQuitEvent
from .spigot import PlayerDeathEvent as SpigotPlayerDeathEvent
from .forge import PlayerCommandEvent as ForgePlayerCommandEvent
from .velocity import DisconnectEvent as VelocityDisconnectEvent
from .velocity import PlayerChatEvent as VelocityPlayerChatEvent
from .fabric import ServerMessageEvent as FabricServerMessageEvent
from .forge import PlayerLoggedInEvent as ForgePlayerLoggedInEvent
from .minecraft import PlayerChatEvent as MinecraftPlayerChatEvent
from .minecraft import PlayerJoinEvent as MinecraftPlayerJoinEvent
from .minecraft import PlayerQuitEvent as MinecraftPlayerQuitEvent
from .forge import PlayerLoggedOutEvent as ForgePlayerLoggedOutEvent
from .spigot import AsyncPlayerChatEvent as SpigotAsyncPlayerChatEvent
from .velocity import CommandExecuteEvent as VelocityCommandExecuteEvent
from .fabric import ServerMessageEvent as FabricServerCommandMessageEvent
from .spigot import PlayerCommandPreprocessEvent as SpigotPlayerCommandPreprocessEvent
from .fabric import ServerPlayConnectionJoinEvent as FabricServerPlayConnectionJoinEvent
from .fabric import (
    ServerLivingEntityAfterDeathEvent as FabricServerLivingEntityAfterDeathEvent,
)
from .fabric import (
    ServerPlayConnectionDisconnectEvent as FabricServerPlayConnectionDisconnectEvent,
)
from .neoforge import (
    ServerChatEvent as NeoForgeServerChatEvent,
    PlayerCommandEvent as NeoForgePlayerCommandEvent,
    PlayerDeathEvent as NeoForgePlayerDeathEvent,
    PlayerLoggedInEvent as NeoForgePlayerLoggedInEvent,
    PlayerLoggedOutEvent as NeoForgePlayerLoggedOutEvent,
    Player as NeoForgePlayer,
)
from .base import (
    Event,
    BasePlayer,
    NoticeEvent,
    MessageEvent,
    BaseChatEvent,
    BaseJoinEvent,
    BaseQuitEvent,
    BaseDeathEvent,
    BasePlayerCommandEvent,
)
