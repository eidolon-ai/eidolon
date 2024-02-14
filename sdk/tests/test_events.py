from eidolon_ai_sdk.io.events import BaseStreamEvent


def test_from_dict():
    BaseStreamEvent.from_dict({"event_type": "user_input", "input": {}})
