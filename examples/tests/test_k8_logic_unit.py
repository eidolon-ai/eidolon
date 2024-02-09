import pytest

from eidolon_examples.k8_monitor.k8_logic_unit import K8LogicUnit


@pytest.mark.asyncio
async def test_core_v1_api():
    found = await K8LogicUnit(spec={}).core_v1_api("list_namespaced_pod", {"namespace": "default", "limit": 20})
    assert found
