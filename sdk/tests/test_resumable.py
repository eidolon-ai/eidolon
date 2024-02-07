import pytest

from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.resources.reference_resource import ReferenceResource
from eidos_sdk.system.resources.resources_base import Metadata
from eidos_sdk.util.replay import replayable, ReplayConfig, replay


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


async def test_resume_point_actually_works(enabled_resume_point_config):
    assert replayable(foo)(1, 2, 3, a=4, b=5) == dict(args=(1, 2, 3), kwargs=dict(a=4, b=5))
    assert len(SideEffect.calls) == 1
    stream = replay(enabled_resume_point_config.save_loc + "/000_foo")
    acc = [s async for s in stream]
    assert acc[0] == dict(args=(1, 2, 3), kwargs=dict(a=4, b=5))
    assert len(SideEffect.calls) == 2
