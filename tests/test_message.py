import pytest

from nonebot.adapters.minecraft import Message, MessageSegment


@pytest.mark.asyncio
async def test_message_escape():
    a = Message([MessageSegment.text("test")])
    assert Message(str(a)) == a

    assert Message() + "test" == Message(MessageSegment.text("test"))
    assert "test" + Message() == Message(MessageSegment.text("test"))

    a = Message()
    a += "test"
    assert a == Message(MessageSegment.text("test"))

    assert MessageSegment.text("test") + "test" == Message([MessageSegment.text("test"), MessageSegment.text("test")])
    assert "test" + MessageSegment.text("test") == Message([MessageSegment.text("test"), MessageSegment.text("test")])
