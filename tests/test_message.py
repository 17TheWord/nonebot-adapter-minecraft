from nonebot.adapters.minecraft import Message, MessageSegment  # type: ignore
from nonebot.adapters.minecraft.models import HoverEvent
import pytest


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


def test_message_segment_text_serializes_hover_event_value_compat():
    segment = MessageSegment.text("hover", hover_event=HoverEvent(action="show_text", contents="tooltip"))

    assert segment.dump() == {
        "text": "hover",
        "hoverEvent": {
            "action": "show_text",
            "contents": "tooltip",
            "value": "tooltip",
        },
    }
