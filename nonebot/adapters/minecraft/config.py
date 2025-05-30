from typing import Dict, List, Union, Optional

from pydantic import Field, BaseModel


class Server(BaseModel):
    enable_rcon: bool = False
    rcon_host: Optional[str] = None
    rcon_port: int = 25575
    rcon_password: str = "password"
    timeout: float = 2.0


class Config(BaseModel):
    minecraft_server_rcon: Dict[str, Server] = Field(default_factory=dict)
    minecraft_ws_urls: Dict[str, List[str]] = Field(default_factory=dict)
    minecraft_access_token: Optional[str] = None
