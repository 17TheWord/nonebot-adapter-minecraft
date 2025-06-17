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

# 原版事件
from .minecraft import (
    Player as MinecraftPlayer,
    PlayerChatEvent as MinecraftPlayerChatEvent,
    PlayerJoinEvent as MinecraftPlayerJoinEvent,
    PlayerQuitEvent as MinecraftPlayerQuitEvent,
)

# Forge 事件
from .forge import (
    Player as ForgePlayer,
    ServerChatEvent as ForgeServerChatEvent,
    PlayerDeathEvent as ForgePlayerDeathEvent,
    PlayerCommandEvent as ForgePlayerCommandEvent,
    PlayerLoggedInEvent as ForgePlayerLoggedInEvent,
    PlayerLoggedOutEvent as ForgePlayerLoggedOutEvent,
)

# Fabric 事件
from .fabric import (
    Player as FabricPlayer,
    ServerMessageEvent as FabricServerMessageEvent,
    ServerCommandMessageEvent as FabricServerCommandMessageEvent,
    ServerPlayConnectionJoinEvent as FabricServerPlayConnectionJoinEvent,
    ServerPlayConnectionDisconnectEvent as FabricServerPlayConnectionDisconnectEvent,
    ServerLivingEntityAfterDeathEvent as FabricServerLivingEntityAfterDeathEvent,
)

# Spigot 事件
from .spigot import (
    Player as SpigotPlayer,
    PlayerJoinEvent as SpigotPlayerJoinEvent,
    PlayerQuitEvent as SpigotPlayerQuitEvent,
    PlayerDeathEvent as SpigotPlayerDeathEvent,
    AsyncPlayerChatEvent as SpigotAsyncPlayerChatEvent,
    PlayerCommandPreprocessEvent as SpigotPlayerCommandPreprocessEvent,
)

# Velocity 事件
from .velocity import (
    LoginEvent as VelocityLoginEvent,
    DisconnectEvent as VelocityDisconnectEvent,
    PlayerChatEvent as VelocityPlayerChatEvent,
    CommandExecuteEvent as VelocityCommandExecuteEvent,
)

# NeoForge 事件
from .neoforge import (
    Player as NeoForgePlayer,
    ServerChatEvent as NeoForgeServerChatEvent,
    PlayerCommandEvent as NeoForgePlayerCommandEvent,
    PlayerDeathEvent as NeoForgePlayerDeathEvent,
    PlayerLoggedInEvent as NeoForgePlayerLoggedInEvent,
    PlayerLoggedOutEvent as NeoForgePlayerLoggedOutEvent,
)

__all__ = [
    # Base
    "Event",
    "BasePlayer",
    "NoticeEvent",
    "MessageEvent",
    "BaseChatEvent",
    "BaseJoinEvent",
    "BaseQuitEvent",
    "BaseDeathEvent",
    "BasePlayerCommandEvent",
    # Minecraft
    "MinecraftPlayer",
    "MinecraftPlayerChatEvent",
    "MinecraftPlayerJoinEvent",
    "MinecraftPlayerQuitEvent",
    # Forge
    "ForgePlayer",
    "ForgeServerChatEvent",
    "ForgePlayerDeathEvent",
    "ForgePlayerCommandEvent",
    "ForgePlayerLoggedInEvent",
    "ForgePlayerLoggedOutEvent",
    # Fabric
    "FabricPlayer",
    "FabricServerMessageEvent",
    "FabricServerCommandMessageEvent",
    "FabricServerPlayConnectionJoinEvent",
    "FabricServerPlayConnectionDisconnectEvent",
    "FabricServerLivingEntityAfterDeathEvent",
    # Spigot
    "SpigotPlayer",
    "SpigotPlayerJoinEvent",
    "SpigotPlayerQuitEvent",
    "SpigotPlayerDeathEvent",
    "SpigotAsyncPlayerChatEvent",
    "SpigotPlayerCommandPreprocessEvent",
    # Velocity
    "VelocityLoginEvent",
    "VelocityDisconnectEvent",
    "VelocityPlayerChatEvent",
    "VelocityCommandExecuteEvent",
    # NeoForge
    "NeoForgePlayer",
    "NeoForgeServerChatEvent",
    "NeoForgePlayerCommandEvent",
    "NeoForgePlayerDeathEvent",
    "NeoForgePlayerLoggedInEvent",
    "NeoForgePlayerLoggedOutEvent",
]
