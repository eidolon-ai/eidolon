import json
import os
from typing import Optional, cast

from eidolon_ai_sdk.builtins.code_builtins import named_builtins
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import for_name
from pydantic import BaseModel


class Group(BaseModel):
    pointer: str
    base: Optional[type]
    additional: list[type] = []


groups = [
    Group(pointer="LLMUnit", base=LLMUnit)
]


def main():
    resources: list[ReferenceResource] = named_builtins()
    for r in resources:
        key = r.metadata.name
        pointer = r.spec
        if not isinstance(pointer, str):
            raise ValueError("Expected pointer of named builtins to be strings")
        try:
            clz = for_name(pointer, object)
        except ValueError:
            print(f"skipping {key}")
            break
        if isinstance(clz, Specable):
            clz = clz.get_spec_type()
        if not isinstance(clz, BaseModel):
            print(f"skipping {key}; not BaseModel")
            break

        json_schema = cast(BaseModel, clz).schema_json
        write_loc = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) / "dist" / f"{key}.json"

        with open(write_loc, 'w') as file:
            json.dump(json_schema, file)






if __name__ == "__main__":
    main()