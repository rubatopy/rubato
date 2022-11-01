"""Test the EventResponse class"""
import pytest
from rubato.utils.radio.events import EventResponse


def test_event_response():
    """Test the EventResponse class"""
    event = EventResponse(1)

    old = {"timestamp": 1}

    assert event["timestamp"] == 1
    assert event.timestamp == 1

    with pytest.raises(KeyError):
        _ = event["test"]

    assert event.get("timestamp") == 1
    assert event.get("test") is None
    assert event.keys() == old.keys()
    assert event.items() == old.items()
    assert list(event.values()) == list(old.values())
