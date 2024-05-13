import json
import os
from pathlib import Path
from typing import cast, Optional

from eidolon_ai_sdk.builtins.code_builtins import named_builtins
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import for_name, fqn
from pydantic import BaseModel


class Group(BaseModel):
    base: type
    default: Optional[str] = None
    components: list[type] = []


groups = {"LLMUnit": Group(base=LLMUnit)}


def main():
    resources: list[ReferenceResource] = named_builtins()
    impls = {}
    for r in resources:
        key = r.metadata.name
        pointer = r.spec
        if isinstance(pointer, dict) and len(pointer) == 1 and "implementation" in pointer:
            pointer = pointer["implementation"]
        if not isinstance(pointer, str):
            raise ValueError("Expected pointer of named builtins to be strings")
        if key in groups:
            groups[key].default = pointer
        else:
            try:
                clz = for_name(pointer, object)
                for g in groups.values():
                    if issubclass(clz, g.base):
                        g.components.append(clz)
            except ValueError as ve:
                print(f"skipping {key}", ve)

    for key, group in groups.items():
        json_schema = cast(BaseModel, clz).model_json_schema()
        write_loc = Path(os.path.dirname(os.path.dirname(__file__))) / "dist" / "component_schemas" / key / "overview.json"
        os.makedirs(os.path.dirname(write_loc), exist_ok=True)

        with open(write_loc, "w") as file:
            json.dump(
                dict(key=key, contract=fqn(group.base), default=group.default, components=group.components),
                file,
                indents=2,
            )

        for component in group.components:
            with open(write_loc, 'w') as file:
                json.dump(json_schema, file, indent=2)


if __name__ == "__main__":
    main()
