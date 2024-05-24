import json
import os
import textwrap
from pathlib import Path
from typing import Optional, Dict, cast, Self

import jsonschema
import jsonschema2md
from pydantic import BaseModel, model_validator

from eidolon_ai_sdk.agent.doc_manager.document_manager import DocumentManager
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.apu import APU
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit, LLMModel
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import for_name


class Group(BaseModel):
    base: type | str
    default: Optional[str] = None
    components: list[tuple[str, type, dict]] = []
    include_root: bool = False
    description: str = None

    def sort_components(self):
        self.components = sorted(self.components, key=lambda x: x[0])

    @model_validator(mode='after')
    def update_description(self) -> Self:
        if not self.description:
            self.description = textwrap.dedent(self.base.__doc__) if self.base.__doc__ else ""
        return self


components_to_load: list[Group] = [
    Group(base="Agents", default="SimpleAgent", components=[
        ("SimpleAgent", SimpleAgent, {}),
        ("RetrieverAgent", RetrieverAgent, {}),
    ]),
    Group(base=APU),
    Group(base=LLMUnit),
    Group(base=LLMModel),
    Group(base=DocumentManager, include_root=True),
    Group(base=DocumentLoader),
]
groups: Dict[str, Group] = {g.base if isinstance(g.base, str) else g.base.__name__: g for g in components_to_load}


def main():
    dist_component_schemas = Path(os.path.dirname(os.path.dirname(__file__))) / "dist" / "component_schemas"
    generate_json(dist_component_schemas)
    write_md(dist_component_schemas)
    update_sitemap()


def update_sitemap(astro_config_loc=Path(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / "webui" / "apps" / "docs" / "astro.config.mjs"):
    with open(astro_config_loc, "r") as astro_config_file:
        lines = astro_config_file.readlines()
    start_index, finish_index = None, None
    for i in range(len(lines)):
        if "### Start Components ###" in lines[i]:
            start_index = i
        if "### End Components ###" in lines[i]:
            finish_index = i
    overview_str_acc = []
    for name, group in groups.items():
        group = cast(Group, group)
        overview_str_acc.extend([
            "{",
            f"  label: '{name}', collapsed: true, items: [",
            f"    {{label: 'Overview', link: '/docs/components/{url_safe(name)}/overview/'}},",
        ])
        for component_name, base, overrides in group.components:
            overview_str_acc.append(
                f"    {{label: '{component_name}', link: '/docs/components/{url_safe(name)}/{url_safe(component_name)}/'}},")
        overview_str_acc.extend([
            "  ]",
            "},"
        ])
    with open(astro_config_loc, "w") as components_file:
        components_file.write(''.join(lines[:start_index + 1]))
        components_file.write("\n".join([" " * 12 + s for s in overview_str_acc]) + "\n")
        components_file.write(''.join(lines[finish_index:]))


def write_md(read_loc, write_loc=Path(os.path.dirname(os.path.dirname(
    os.path.dirname(__file__)))) / "webui" / "apps" / "docs" / "src" / "content" / "docs" / "docs" / "components"):
    for k, g in groups.items():
        write_file_loc = write_loc / url_safe(k) / "overview.md"
        title = f"{k} Overview"
        description = f"Overview of {k} components"
        content = [f"## Builtins"]
        for name, clz, overrides in g.components:
            content.append(f"* [{name}](/docs/components/{url_safe(k)}/{url_safe(name)}/)")
        write_astro_md_file(g.description + "\n" + "\n".join(content), description, title, write_file_loc)

    for component in os.listdir(read_loc):
        for file in os.listdir(read_loc / component):
            write_file_loc = write_loc / url_safe(component) / (url_safe(file.replace(".json", "")) + ".md")
            parser = jsonschema2md.Parser(examples_as_yaml=True)
            with open(read_loc / component / file, 'r') as json_file:
                obj = json.load(json_file)
            title = obj.get('title', file)
            description = f"Description of {title} component"
            md_lines = parser.parse_schema(obj)[1:]  # remove title
            content = ''.join(md_lines)
            write_astro_md_file(content, description, title, write_file_loc)


def write_astro_md_file(content, description, title, write_file_loc):
    for name, group in groups.items():
        content = content.replace(f"Reference[{name}]", f"[Reference[{name}]](/docs/components/{url_safe(name)}/overview/)")
    os.makedirs(os.path.dirname(write_file_loc), exist_ok=True)
    md_str = f"""---
title: {title}
description: {description}
---
""" + content
    with open(write_file_loc, 'w') as md_file:
        md_file.write(md_str)


def generate_json(write_base):
    resources: list[ReferenceResource] = AgentOS.get_resources(ReferenceResource).values()
    for r in resources:
        key = r.metadata.name
        overrides = Reference[object, key]._transform(r.spec)
        pointer = overrides.pop("implementation")
        if key in groups:
            groups[key].default = pointer
        try:
            clz = for_name(pointer, object)
            for k, g in groups.items():
                if not isinstance(g.base, str) and (issubclass(clz, g.base) or clz == g.base) and (
                        k != key or g.include_root):
                    g.components.append((key, clz, overrides))
                    g.sort_components()
        except ValueError as ve:
            print(f"skipping {key}", ve)
    for key, group in groups.items():
        write_loc = write_base / key
        os.makedirs(os.path.dirname(write_loc / "overview.json"), exist_ok=True)
        for name, clz, overrides in group.components:
            if hasattr(clz, "model_json_schema"):
                json_schema = clz.model_json_schema()
                to_pop = set()
                # todo, this should be part of reference json schema
                for k, v in json_schema.get("$defs", {}).items():
                    if "_Reference" in k:
                        to_pop.add(k)
                        del v["properties"]
                        del v["additionalProperties"]

                json_schema = inline_refs(json_schema)
                for k, v in json_schema['properties'].items():
                    if k in overrides:
                        v['default'] = overrides[k]
                json_schema['title'] = name

                for r in to_pop:
                    del json_schema["$defs"][r]
                if "$defs" in json_schema and not json_schema["$defs"]:
                    del json_schema["$defs"]
                with open(write_loc / (name + ".json"), 'w') as file:
                    json.dump(json_schema, file, indent=2)
            else:
                print(f"Skipping non BaseModel component {name}")


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


def url_safe(name: str) -> str:
    return name.replace(" ", "_").replace(".", "_").lower()


if __name__ == "__main__":
    main()
