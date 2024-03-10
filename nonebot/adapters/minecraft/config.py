from typing import Dict

from pydantic import BaseModel, Field


class Server(BaseModel):
    enable_rcon: bool = False
    rcon_port: int = 25575
    rcon_password: str = "password"


class Config(BaseModel):
    minecraft_server_rcon: Dict[str, Server] = Field(default_factory=dict)
