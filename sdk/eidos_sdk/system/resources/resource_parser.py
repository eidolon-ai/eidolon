from eidos_sdk.system.resources.agent_resource import AgentResource
from eidos_sdk.system.resources.machine_resource import MachineResource
from eidos_sdk.system.resources.eidos_ref_resource import EidosRef

_kinds = {r.kind_literal(): r for r in [MachineResource, AgentResource, EidosRef]}


def parse_resource(d: dict):
    if d.get("kind") not in _kinds:
        raise ValueError(f"Unknown kind {d.get('kind')}, valid kinds are {list(_kinds.keys())}")
    else:
        return _kinds[d["kind"]].model_validate(d)