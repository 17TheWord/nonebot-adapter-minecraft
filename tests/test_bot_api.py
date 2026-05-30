from nonebot.adapters.minecraft import Bot, Message, MessageSegment
from nonebot.adapters.minecraft.exception import ActionFailed
import pytest


class FakeAdapter:
    def __init__(self):
        self.calls = []

    async def send_websocket_message(self, bot_id, api, data):
        self.calls.append((bot_id, api, data))
        if api == "send_rcon_command":
            return "command result"
        return None


def make_bot():
    return Bot(FakeAdapter(), "Server")


@pytest.mark.asyncio
async def test_send_msg_serializes_string():
    bot = make_bot()

    await Bot.send_msg(bot, "hello")

    assert bot.adapter.calls == [("Server", "send_msg", {"message": {"text": "hello"}})]


@pytest.mark.asyncio
async def test_send_msg_serializes_message():
    bot = make_bot()
    message = Message([MessageSegment.text("hello"), MessageSegment.text("world", color="gold")])

    await Bot.send_msg(bot, message)

    assert bot.adapter.calls == [
        (
            "Server",
            "send_msg",
            {"message": [{"text": "hello"}, {"text": "world", "color": "gold"}]},
        )
    ]


@pytest.mark.asyncio
async def test_send_title_requires_title_or_subtitle():
    bot = make_bot()

    with pytest.raises(ActionFailed):
        await Bot.send_title(bot)


@pytest.mark.asyncio
async def test_send_title_serializes_payload():
    bot = make_bot()

    await Bot.send_title(bot, title="title", subtitle=MessageSegment.text("subtitle"), fade_in=1, stay=2, fade_out=3)

    assert bot.adapter.calls == [
        (
            "Server",
            "send_title",
            {
                "title": {"text": "title"},
                "subtitle": {"text": "subtitle"},
                "fade_in": 1,
                "stay": 2,
                "fade_out": 3,
            },
        )
    ]


@pytest.mark.asyncio
async def test_send_actionbar_serializes_message_segment():
    bot = make_bot()

    await Bot.send_actionbar(bot, MessageSegment.text("action", bold=True))

    assert bot.adapter.calls == [("Server", "send_actionbar", {"message": {"text": "action", "bold": True}})]


@pytest.mark.asyncio
async def test_send_rcon_command_returns_result():
    bot = make_bot()

    result = await Bot.send_rcon_command(bot, "list")

    assert result == "command result"
    assert bot.adapter.calls == [("Server", "send_rcon_command", {"command": "list"})]
