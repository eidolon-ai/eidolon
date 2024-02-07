import pytest

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.replay import replayable, ReplayConfig, replay, default_serializer


class SideEffect:
    calls = []


def foo(*args, **kwargs):
    SideEffect.calls.append(dict(args=args, kwargs=kwargs))
    return SideEffect.calls[-1]


@pytest.fixture(autouse=True)
def side_effect_manager():
    SideEffect.cals = []
    yield
    SideEffect.cals = []


@pytest.fixture
def enabled_resume_point_config(machine, request):
    AgentOS.register_resource(
        ReferenceResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name=ReplayConfig.__name__),
            spec=dict(save_loc=f"resume_points/{request.node.name}"),
        )
    )
    return AgentOS.get_instance(ReplayConfig)


def test_default_resume_point_config(machine):
    assert AgentOS.get_instance(ReplayConfig).save_loc is None


def test_resume_point_enabled(enabled_resume_point_config):
    assert enabled_resume_point_config.save_loc is not None


async def test_resume_point_actually_works(enabled_resume_point_config, file_memory_loc):
    assert replayable(foo)(1, 2, 3, a=4, b=5) == dict(args=(1, 2, 3), kwargs=dict(a=4, b=5))
    assert len(SideEffect.calls) == 1

    stream = replay(file_memory_loc / enabled_resume_point_config.save_loc / "000_foo")
    acc = [s async for s in stream]
    assert acc[0] == dict(args=(1, 2, 3), kwargs=dict(a=4, b=5))
    assert len(SideEffect.calls) == 2


bad_obj = {'args': [], 'kwargs': {'messages': [{'role': 'system', 'content': "You are an football expert with a focus on Travis Kelce. You love the game and enjoy helping new fans learn.\nYou speak in a friendly, helpful tone and are always willing to answer questions.\n\nTaylor Swift and Travis Kelce are in a new, public relationship. This is public knowledge and you are happy to \ntalk about it.\n\nYou want to help Taylor's fans (swifties) learn more about the football. Since you are an expert, it is your \nresponsibility to research questions so that you have answers for the users. You will have the ability to search \nthe web and visit websites to find answers to questions.\n\nUse these capabilities to retrieve up-to-date information as needed.\nYou may make multiple searches to answer questions. When responding, add specific citations to your response.\n\nIf you get see system messages suggesting feedback, incorporate it as fact."}, {'role': 'user', 'content': [{'type': 'text', 'text': 'what is football?\n\nBe concise.'}]}], 'model': 'gpt-4-1106-preview', 'temperature': 0.3, 'tools': [{'type': 'function', 'function': {'name': 'WebSearch_go_to_url', 'description': '\n        Retrieve the html document from a given webpage\n        :param url: the url to retrieve.\n        :return: the html document.\n        ', 'parameters': {'properties': {'url': {'title': 'Url', 'type': 'string'}}, 'required': ['url'], 'title': 'Go_to_urlInputModel', 'type': 'object'}}}, {'type': 'function', 'function': {'name': 'WebSearch_search', 'description': '\n        Search google and get the results. Cannot return more than 100 results\n        :param term: the search query\n        :param num_results: the number of results to return (default 10, max 100)\n        :param lang: the language to search in (default en)\n        :return: A list of SearchResults including url, title, and description\n        ', 'parameters': {'properties': {'term': {'title': 'Term', 'type': 'string'}, 'num_results': {'default': 10, 'title': 'Num Results', 'type': 'integer'}, 'lang': {'default': 'en', 'title': 'Lang', 'type': 'string'}}, 'required': ['term'], 'title': 'SearchInputModel', 'type': 'object'}}}], 'stream': True}}


async def test_default_yaml_parser():
    str_repr, _ = default_serializer(bad_obj)
    assert str_repr.count("\\n") < 20
    assert str_repr.count("|") == 4
