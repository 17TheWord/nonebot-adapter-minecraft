from pydantic import BaseModel, Field


class Server(BaseModel):
    enable_rcon: bool = False
    rcon_host: str | None = None
    rcon_port: int = 25575
    rcon_password: str = "password"
    timeout: float = 2.0


class Config(BaseModel):
    minecraft_server_rcon: dict[str, Server] = Field(default_factory=dict)
    minecraft_ws_urls: dict[str, list[str]] = Field(default_factory=dict)
    minecraft_access_token: str | None = None
