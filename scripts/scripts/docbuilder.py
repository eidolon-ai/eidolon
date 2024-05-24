import json
import os
from pathlib import Path
from typing import Optional

import jsonschema
from pydantic import BaseModel

from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.apu import APU
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import for_name, fqn


class Group(BaseModel):
    base: type
    default: Optional[str] = None
    components: list[tuple[type, dict]] = []


groups: dict[str, Group] = {
    "LLMUnit": Group(base=LLMUnit),
    "Agents": Group(base=object, default="SimpleAgent", components=[
        (SimpleAgent, {}),
        (RetrieverAgent, {}),
    ]),
    "APU": Group(base=APU),
}


def main():
    generate_json()


def generate_json():
    resources: list[ReferenceResource] = AgentOS.get_resources(ReferenceResource).values()
    for r in resources:
        key = r.metadata.name
        overrides = Reference[object, key]._transform(r.spec)
        pointer = overrides.pop("implementation")
        if key in groups:
            groups[key].default = pointer
        else:
            try:
                clz = for_name(pointer, object)
                for g in groups.values():
                    if issubclass(clz, g.base) and g.base != object:
                        g.components.append((clz, overrides))
            except ValueError as ve:
                print(f"skipping {key}", ve)
    for key, group in groups.items():
        write_loc = Path(os.path.dirname(os.path.dirname(__file__))) / "dist" / "component_schemas" / key
        os.makedirs(os.path.dirname(write_loc / "overview.json"), exist_ok=True)

        with open(write_loc / "overview.json", "w") as file:
            components = [c.__name__ for c, _ in group.components]
            json.dump(
                dict(key=key, contract=fqn(group.base), default=group.default, components=components), file, indent=2
            )

        for component, overrides in group.components:
            if hasattr(component, "model_json_schema"):
                json_schema = component.model_json_schema()

                to_pop = set()
                # todo, this should be part of reference json schema
                for k, v in json_schema.get("$defs", {}).items():
                    if "_Reference" in k:
                        to_pop.add(k)
                        del v["properties"]
                        del v["additionalProperties"]

                json_schema = inline_refs(json_schema)
                json_schema['overrides'] = overrides
                for r in to_pop:
                    del json_schema["$defs"][r]
                if "$defs" in json_schema and not json_schema["$defs"]:
                    del json_schema["$defs"]
                with open(write_loc / (component.__name__ + ".json"), 'w') as file:
                    json.dump(json_schema, file, indent=2)
            else:
                print(f"Skipping non BaseModel component {component}")


def inline_refs(schema, resolver=None):
    if resolver is None:
        resolver = jsonschema.RefResolver.from_schema(schema)

    if isinstance(schema, dict):
        if "$ref" in schema and "_Reference" in schema["$ref"]:
            with resolver.resolving(schema["$ref"]) as resolved:
                return inline_refs(resolved, resolver)
        else:
            return {k: inline_refs(v, resolver) for k, v in schema.items()}
    elif isinstance(schema, list):
        return [inline_refs(i, resolver) for i in schema]
    else:
        return schema




if __name__ == "__main__":
    main()
