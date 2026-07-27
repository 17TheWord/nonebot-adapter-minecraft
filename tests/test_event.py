import asyncio
from typing import Literal

import nonebot
from nonebot.adapters.minecraft import (  # type: ignore
    Adapter,
    Bot,
    Event,
    Message,
    MessageSegment,
    Player,
    PlayerChatEvent,
)
from nonebot.compat import model_dump
from nonebot.log import logger
import pytest


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


def test_json_to_event_returns_none_for_non_dict():
    assert Adapter.json_to_event("invalid") is None


@pytest.mark.asyncio
async def test_json_to_event_stores_response_payload():
    future = asyncio.get_event_loop().create_future()
    Adapter._result_store._futures[1] = future

    try:
        parsed = Adapter.json_to_event({"post_type": "response", "echo": "1", "status": "OK", "data": "result"})
    finally:
        Adapter._result_store._futures.pop(1, None)

    assert parsed is None
    assert future.result() == {"post_type": "response", "echo": "1", "status": "OK", "data": "result"}


def test_json_to_event_returns_none_when_parse_fails():
    assert Adapter.json_to_event({"post_type": "notice"}) is None


@pytest.mark.asyncio
async def test_bot_handle_event_checks_nickname(app, monkeypatch):
    adapter = nonebot.get_adapter(Adapter)
    bot = Bot(adapter, "Server")
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
        player=Player(nickname="Steve"),
        message=Message("Bot, hello"),
    )
    handled = []

    async def fake_handle_event(bot, event):
        handled.append((bot, event))

    monkeypatch.setattr(bot.config, "nickname", {"Bot"})
    monkeypatch.setattr("nonebot.adapters.minecraft.bot.handle_event", fake_handle_event)

    await bot.handle_event(event)

    assert event.to_me is True
    assert str(event.message) == "hello"
    assert handled == [(bot, event)]


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
