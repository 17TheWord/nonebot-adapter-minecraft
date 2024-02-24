from typing import Dict, Optional

from pydantic import BaseModel, Field


class Server(BaseModel):
    enable_rcon: Optional[bool] = False
    rcon_port: Optional[int] = 25575
    rcon_password: Optional[str] = "password"


class Config(BaseModel):
    minecraft_server_rcon: Dict[str, Server] = Field(default_factory=dict)
