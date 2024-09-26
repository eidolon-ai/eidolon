import copy
import json
import os
import shutil
import textwrap
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, Dict, Self, cast, List

from jinja2 import Environment, StrictUndefined
from json_schema_for_humans.generate import generate_from_schema
from json_schema_for_humans.generation_configuration import GenerationConfiguration
from pydantic import BaseModel, model_validator

from eidolon_ai_sdk.agent.api_agent import APIAgent
from eidolon_ai_sdk.agent.doc_manager.document_manager import DocumentManager
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent.sql_agent.agent import SqlAgent
from eidolon_ai_sdk.agent_os_interfaces import SimilarityMemory, SymbolicMemory
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMModel
from eidolon_ai_sdk.apu.logic_unit import LogicUnit
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.system.agent_machine import AgentMachine
from eidolon_ai_sdk.system.kernel import AgentOSKernel
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Resource
from eidolon_ai_sdk.util.class_utils import for_name


class Group(BaseModel):
    base: type | str
    components: list[tuple[str, type, dict]] = []
    description: str = None
    document_in_sidebar: bool = True
    default: Optional[str] = None

    def sort_components(self):
        self.components = sorted(self.components, key=lambda x: x[0])

    @model_validator(mode='after')
    def update_description(self) -> Self:
        if not self.description:
            if isinstance(self.base, type) and self.base.__doc__:
                self.description = textwrap.dedent(self.base.__doc__).strip()
            elif isinstance(self.base, type):
                self.description = f"Overview of {self.base.__name__} components"
            else:
                self.description = f"Overview of {self.base} components"
        return self

    def get_components(self):
        self.sort_components()
        return self.components


EIDOLON = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def main():
    print("Generating docs...")
    dist_component_schemas = EIDOLON / "scripts" / "scripts" / "docbuilder" / "schemas"
    schema = SimpleAgent.model_json_schema()
    print("json generated")
    shutil.rmtree(dist_component_schemas, ignore_errors=True)
    defs = schema.get("$defs", {})
    transform_file_defs(schema, defs)
    for k, v in defs.items():
        write_loc = get_write_loc(v)
        if write_loc:
            copied = copy.deepcopy(v)
            local_refs = find_local_refs(v)
            relative_write_locs(copied, "../" + str(write_loc.parent) + "/")

            if local_refs:
                copied["$defs"] = {ref.removeprefix("#/$defs/"): defs[ref.removeprefix("#/$defs/")] for ref in local_refs}
            os.makedirs((dist_component_schemas / write_loc).parent, exist_ok=True)
            with open(dist_component_schemas / write_loc, 'w') as json_file:
                json.dump(copied, json_file, indent=2)
    print("json written")


    # write_md(dist_component_schemas)
    # update_sitemap()


def get_write_loc(schema):
    if "reference_pointer" in schema:  # group, should only be referenced by component
        return Path(f"{schema['reference_pointer']['type']}/overview.json")
    elif 'reference_details' in schema:  # component definition, should only be referenced by groups
        return Path(f"{schema['reference_details']['group']}/{schema['reference_details']['name']}.json")
    else:
        return None


def relative_write_locs(schema, loc):
    if isinstance(schema, dict):
        if "$ref" in schema:
            schema["$ref"] = schema["$ref"].replace(loc, "./")
        for v in schema.values():
            relative_write_locs(v, loc)
    elif isinstance(schema, list):
        for i in schema:
            relative_write_locs(i, loc)


def transform_file_defs(schema, defs):
    if isinstance(schema, dict):
        if "$ref" in schema:
            ref_key = schema["$ref"].removeprefix("#/$defs/")
            write_loc = get_write_loc(defs[ref_key])
            if write_loc:
                schema['$ref'] = "../" + str(write_loc)
        for v in schema.values():
            transform_file_defs(v, defs)
    elif isinstance(schema, list):
        for i in schema:
            transform_file_defs(i, defs)


def find_local_refs(schema) -> List[str]:
    if isinstance(schema, dict):
        if "$ref" in schema:
            return [schema["$ref"]] if schema["$ref"].startswith("#/$defs/") else []
        else:
            return [ref for v in schema.values() for ref in find_local_refs(v)]
    elif isinstance(schema, list):
        return [ref for i in schema for ref in find_local_refs(i)]
    else:
        return []


def update_sitemap(astro_config_loc=EIDOLON / "webui" / "apps" / "docs" / "astro.config.mjs"):
    with open(astro_config_loc, "r") as astro_config_file:
        lines = astro_config_file.readlines()
    start_index, finish_index = None, None
    for i in range(len(lines)):
        if "### Start Components ###" in lines[i]:
            start_index = i
        if "### End Components ###" in lines[i]:
            finish_index = i
    args = [dict(name=name, safe_name=url_safe(name), components=[
        dict(name=c_name, safe_name=url_safe(c_name)) for c_name, _, _ in g.get_components()
    ]) for name, g in groups.items() if g.document_in_sidebar]
    templated = template("template_sitemap_mjs", groups=args)

    with open(astro_config_loc, "w") as components_file:
        components_file.write(''.join(lines[:start_index + 1]))
        components_file.write(templated)
        components_file.write(''.join(lines[finish_index:]))


cut_after_str = """|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
"""


def write_md(read_loc,
             write_loc=EIDOLON / "webui" / "apps" / "docs" / "src" / "content" / "docs" / "docs" / "components"):
    shutil.rmtree(write_loc, ignore_errors=True)
    for k, g in groups.items():
        write_file_loc = write_loc / url_safe(k) / "overview.md"
        title = f"{k} Overview"
        content = ["## Builtins"]
        for name, _, _ in g.get_components():
            content.append(f"* [{name}](/docs/components/{url_safe(k)}/{url_safe(name)}/)")
            if name == g.default:
                content[-1] += " (default)"
        with open(read_loc / k / "overview.json", 'r') as json_file:
            description = json.load(json_file)['description']
        write_astro_md_file(g.description + "\n" + "\n".join(content), description, title, write_file_loc)

    with TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        shutil.copytree(read_loc, tempdir, dirs_exist_ok=True)
        for root, dirs, files in os.walk(tempdir):
            for file in files:
                with open(os.path.join(root, file), 'r') as json_file:
                    obj = json.load(json_file)
                    clean_ref_groups_for_md(obj)
                with open(os.path.join(root, file), 'w') as json_file:
                    json.dump(obj, json_file, indent=2)

        for k, g in groups.items():
            for component, _, _ in g.get_components():
                write_file_loc = write_loc / url_safe(k) / (url_safe(component.replace(".json", "")) + ".md")
                with open(tempdir / k / (component + ".json"), 'r') as json_file:
                    obj = json.load(json_file)
                    title = obj.get('title', component)
                    description = f"Description of {title} component"
                content = generate_from_schema(tempdir / k / (component + ".json"), config=GenerationConfiguration(
                    show_breadcrumbs=False,
                    template_name="md",
                    with_footer=False,
                ))

                content = content[(content.index(cut_after_str) + len(cut_after_str)):]
                # for name in groups.keys():
                #     content = content.replace(f"`[Reference[{name}]](/docs/components/{url_safe(name)}/overview)`",
                #                               f"[`Reference[{name}]`](/docs/components/{url_safe(name)}/overview)")

                write_astro_md_file(content, description, title, write_file_loc)


def write_astro_md_file(content, description, title, write_file_loc):
    for name, group in groups.items():
        content = content.replace(f"../{name}/overview.json",
                                  f"[{name}](/docs/components/{url_safe(name)}/overview)")
    os.makedirs(os.path.dirname(write_file_loc), exist_ok=True)

    md_str = template("template_component_md", title=title, description=description, content=content)
    with open(write_file_loc, 'w') as md_file:
        md_file.write(md_str)


def template(template_file, **kwargs):
    with open(EIDOLON / "scripts" / "scripts" / "docbuilder" / template_file) as template:
        return Environment(undefined=StrictUndefined).from_string(template.read()).render(**kwargs)


def generate_json(write_base):
    schema = SimpleAgent.model_json_schema()
    print(schema)


def inline_refs(schema, defs):
    if isinstance(schema, dict):
        if "$ref" in schema and "_Reference" in schema["$ref"]:
            return defs[schema["$ref"].replace("#/$defs/", "")]
        else:
            return {k: inline_refs(v, defs) for k, v in schema.items()}
    elif isinstance(schema, list):
        return [inline_refs(i, defs) for i in schema]
    else:
        return schema


def clean_ref_groups_for_md(schema, seen=None):
    seen = seen or set()
    if id(schema) in seen:
        return
    if isinstance(schema, dict):  # inline optional types for easier to read markdown
        if "anyOf" in schema and len(schema['anyOf']) == 2 and [s for s in schema['anyOf'] if len(s) == 1 and s.get("type") == "null"] and schema.get('default') is None:
            any_of = schema.pop('anyOf')
            object_type = [s for s in any_of if not (len(s) == 1 and s.get("type") == "null")][0]
            schema.update(object_type)
        if "reference_group" in schema:
            if "anyOf" in schema:
                del schema['anyOf']
                schema['type'] = f"Reference[{schema['reference_group']['type']}]"
        else:
            for v in schema.values():
                clean_ref_groups_for_md(v, {id(schema), *seen})
    elif isinstance(schema, list):
        for i in schema:
            clean_ref_groups_for_md(i, {id(schema), *seen})
    else:
        pass


def url_safe(name: str) -> str:
    return name.replace(" ", "_").replace(".", "_").lower()


if __name__ == "__main__":
    main()
