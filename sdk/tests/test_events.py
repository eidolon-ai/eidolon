from eidolon_ai_client.events import BaseStreamEvent


def test_from_dict():
    BaseStreamEvent.from_dict({"event_type": "user_input", "input": {}})
