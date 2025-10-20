from pydantic import BaseModel, Field


class Config(BaseModel):
    minecraft_ws_urls: dict[str, list[str]] = Field(default_factory=dict)
    minecraft_access_token: str | None = None
