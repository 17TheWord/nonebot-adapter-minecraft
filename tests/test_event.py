import json
from pathlib import Path
from typing import Literal

import pytest
from nonebot.log import logger
from nonebot.compat import model_dump

from nonebot.adapters.minecraft import (
    Event,
    Adapter,
    SpigotPlayer,
    MessageSegment,
    SpigotAsyncPlayerChatEvent,
)


@pytest.mark.asyncio
async def test_event():
    class MessageSelfEvent(Event):
        post_type: Literal["message_self"]

    event = MessageSelfEvent(
        timestamp=0,
        server_name="Server",
        post_type="message_self",
        event_name="MessageSelfEvent",
        sub_type="test",
    )

    Adapter.add_custom_model(MessageSelfEvent)
    parsed = Adapter.json_to_event(model_dump(event))
    assert parsed == event


@pytest.mark.asyncio
async def test_event_log():
    msg = MessageSegment.text(text="[text]") + MessageSegment.actionbar(
        text="[actionbar]"
    )
    event = SpigotAsyncPlayerChatEvent(
        timestamp=0,
        post_type="message",
        event_name="AsyncPlayerChatEvent",
        server_name="Server",
        sub_type="chat",
        message_id="",
        to_me=False,
        ori_message=msg,
        player=SpigotPlayer(nickname="test"),
        message=msg,
    )
    logger.opt(colors=True).success(
        f"{event.get_event_name()}: {event.get_event_description()}"
    )
