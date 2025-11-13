from typing import Literal

import pytest

from nonebot.adapters.minecraft import (  # type: ignore
    Adapter,
    Event,
    Message,
    MessageSegment,
    Player,
    PlayerChatEvent,
)
from nonebot.compat import model_dump
from nonebot.log import logger


@pytest.mark.asyncio
async def test_event():
    class MessageSelfEvent(Event):
        post_type: Literal["message_self"]

    event = MessageSelfEvent(
        timestamp=0,
        server_name="Server",
        post_type="message_self",
        server_version="1.20.1",
        server_type="spigot",
        event_name="MessageSelfEvent",
        sub_type="test",
    )

    Adapter.add_custom_model(MessageSelfEvent)
    parsed = Adapter.json_to_event(model_dump(event))
    assert parsed == event


@pytest.mark.asyncio
async def test_event_log():
    msg = Message(MessageSegment.text(text="[text]"))
    event = PlayerChatEvent(
        timestamp=0,
        post_type="message",
        event_name="PlayerChatEvent",
        server_name="Server",
        sub_type="player_chat",
        message_id="",
        server_version="1.20.1",
        server_type="spigot",
        to_me=False,
        player=Player(nickname="test"),
        message=msg,
    )
    logger.opt(colors=True).success(f"{event.get_event_name()}: {event.get_event_description()}")
