from .base import (
    BaseChatEvent,
    BaseDeathEvent,
    BaseJoinEvent,
    BasePlayer,
    BasePlayerCommandEvent,
    BaseQuitEvent,
    Event,
    MessageEvent,
    NoticeEvent,
)

# Fabric 事件
from .fabric import Player as FabricPlayer
from .fabric import ServerCommandMessageEvent as FabricServerCommandMessageEvent
from .fabric import ServerLivingEntityAfterDeathEvent as FabricServerLivingEntityAfterDeathEvent
from .fabric import ServerMessageEvent as FabricServerMessageEvent
from .fabric import ServerPlayConnectionDisconnectEvent as FabricServerPlayConnectionDisconnectEvent
from .fabric import ServerPlayConnectionJoinEvent as FabricServerPlayConnectionJoinEvent

# Folia 事件
from .folia import AsyncPlayerChatEvent as FoliaAsyncPlayerChatEvent
from .folia import Player as FoliaPlayer
from .folia import PlayerCommandPreprocessEvent as FoliaPlayerCommandPreprocessEvent
from .folia import PlayerDeathEvent as FoliaPlayerDeathEvent
from .folia import PlayerJoinEvent as FoliaPlayerJoinEvent
from .folia import PlayerQuitEvent as FoliaPlayerQuitEvent

# Forge 事件
from .forge import Player as ForgePlayer
from .forge import PlayerCommandEvent as ForgePlayerCommandEvent
from .forge import PlayerDeathEvent as ForgePlayerDeathEvent
from .forge import PlayerLoggedInEvent as ForgePlayerLoggedInEvent
from .forge import PlayerLoggedOutEvent as ForgePlayerLoggedOutEvent
from .forge import ServerChatEvent as ForgeServerChatEvent

# 原版事件
from .minecraft import Player as MinecraftPlayer
from .minecraft import PlayerChatEvent as MinecraftPlayerChatEvent
from .minecraft import PlayerJoinEvent as MinecraftPlayerJoinEvent
from .minecraft import PlayerQuitEvent as MinecraftPlayerQuitEvent

# NeoForge 事件
from .neoforge import Player as NeoForgePlayer
from .neoforge import PlayerCommandEvent as NeoForgePlayerCommandEvent
from .neoforge import PlayerDeathEvent as NeoForgePlayerDeathEvent
from .neoforge import PlayerLoggedInEvent as NeoForgePlayerLoggedInEvent
from .neoforge import PlayerLoggedOutEvent as NeoForgePlayerLoggedOutEvent
from .neoforge import ServerChatEvent as NeoForgeServerChatEvent
from .spigot import AsyncPlayerChatEvent as SpigotAsyncPlayerChatEvent

# Spigot 事件
from .spigot import Player as SpigotPlayer
from .spigot import PlayerCommandPreprocessEvent as SpigotPlayerCommandPreprocessEvent
from .spigot import PlayerDeathEvent as SpigotPlayerDeathEvent
from .spigot import PlayerJoinEvent as SpigotPlayerJoinEvent
from .spigot import PlayerQuitEvent as SpigotPlayerQuitEvent
from .velocity import CommandExecuteEvent as VelocityCommandExecuteEvent
from .velocity import DisconnectEvent as VelocityDisconnectEvent

# Velocity 事件
from .velocity import LoginEvent as VelocityLoginEvent
from .velocity import PlayerChatEvent as VelocityPlayerChatEvent

__all__ = [
    "BaseChatEvent",
    "BaseDeathEvent",
    "BaseJoinEvent",
    "BasePlayer",
    "BasePlayerCommandEvent",
    "BaseQuitEvent",
    # Base
    "Event",
    # Fabric
    "FabricPlayer",
    "FabricServerCommandMessageEvent",
    "FabricServerLivingEntityAfterDeathEvent",
    "FabricServerMessageEvent",
    "FabricServerPlayConnectionDisconnectEvent",
    "FabricServerPlayConnectionJoinEvent",
    # Folia
    "FoliaAsyncPlayerChatEvent",
    "FoliaPlayer",
    "FoliaPlayerCommandPreprocessEvent",
    "FoliaPlayerDeathEvent",
    "FoliaPlayerJoinEvent",
    "FoliaPlayerQuitEvent",
    # Forge
    "ForgePlayer",
    "ForgePlayerCommandEvent",
    "ForgePlayerDeathEvent",
    "ForgePlayerLoggedInEvent",
    "ForgePlayerLoggedOutEvent",
    "ForgeServerChatEvent",
    "MessageEvent",
    # Minecraft
    "MinecraftPlayer",
    "MinecraftPlayerChatEvent",
    "MinecraftPlayerJoinEvent",
    "MinecraftPlayerQuitEvent",
    # NeoForge
    "NeoForgePlayer",
    "NeoForgePlayerCommandEvent",
    "NeoForgePlayerDeathEvent",
    "NeoForgePlayerLoggedInEvent",
    "NeoForgePlayerLoggedOutEvent",
    "NeoForgeServerChatEvent",
    "NoticeEvent",
    "SpigotAsyncPlayerChatEvent",
    # Spigot
    "SpigotPlayer",
    "SpigotPlayerCommandPreprocessEvent",
    "SpigotPlayerDeathEvent",
    "SpigotPlayerJoinEvent",
    "SpigotPlayerQuitEvent",
    "VelocityCommandExecuteEvent",
    "VelocityDisconnectEvent",
    # Velocity
    "VelocityLoginEvent",
    "VelocityPlayerChatEvent",
]
