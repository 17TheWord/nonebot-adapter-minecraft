from nonebot.adapters.minecraft.models import HoverEvent, HoverShowItem


def test_hover_event_syncs_value_from_contents():
    event = HoverEvent(action="show_text", contents="hello")

    assert event.contents == "hello"
    assert event.value == "hello"


def test_hover_event_syncs_contents_from_value():
    event = HoverEvent(action="show_text", value="hello")

    assert event.contents == "hello"
    assert event.value == "hello"


def test_hover_event_preserves_explicit_contents_and_value():
    event = HoverEvent(action="show_text", contents="new", value="old")

    assert event.contents == "new"
    assert event.value == "old"


def test_hover_event_syncs_complex_content():
    item = HoverShowItem(id="minecraft:diamond", count=1)
    event = HoverEvent(action="show_item", contents=item)

    assert event.contents == item
    assert event.value == item


def test_hover_event_assignment_syncs_fields():
    event = HoverEvent(action="show_text")

    event.contents = "hello"

    assert event.value == "hello"


def test_hover_event_assignment_preserves_explicit_content():
    event = HoverEvent(action="show_text", contents="hello")

    event.value = "world"

    assert event.contents == "hello"
    assert event.value == "world"
