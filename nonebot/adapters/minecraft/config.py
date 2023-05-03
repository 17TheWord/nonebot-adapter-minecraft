from typing import Dict

from pydantic import Extra, BaseModel, Field


class Server(BaseModel):
    enable_rcon: bool = False
    rcon_port: int
    rcon_password: str


class Config(BaseModel):
    minecraft_server_rcon: Dict[str, Server] = Field(default_factory=dict)

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True
