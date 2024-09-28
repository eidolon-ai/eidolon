import copy
import json
import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from jinja2 import Environment, StrictUndefined
from json_schema_for_humans.generate import generate_from_schema
from json_schema_for_humans.generation_configuration import GenerationConfiguration
from pydantic import BaseModel

from eidolon_ai_sdk.agent.api_agent import APIAgent
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent.sql_agent.agent import SqlAgent
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource

EIDOLON = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def main():
    dist_component_schemas = EIDOLON / "scripts" / "scripts" / "docbuilder" / "schemas"

    print("Generating json...")
    json_schema = generate_schema()

    print("writing json...")
    shutil.rmtree(dist_component_schemas, ignore_errors=True)
    write_json_schema(dist_component_schemas, json_schema)

    print("writing md...")
    write_md(dist_component_schemas)

    print("updating sitemap...")
    update_sitemap()


class AgentBuilder(BaseModel):
    documented_agents: Reference["Agent", "SimpleAgent", SimpleAgent | RetrieverAgent | APIAgent | SqlAgent]


def generate_schema():
    accumulated_schema = {"$defs": {}}

    machine_schema = MachineResource.model_json_schema()
    accumulated_schema["$defs"].update(machine_schema.pop("$defs", {}))
    fake_agent_schema = AgentBuilder.model_json_schema()
    accumulated_schema["$defs"].update(fake_agent_schema.pop("$defs", {}))
    return accumulated_schema


def write_json_schema(dist_component_schemas, schema):
    defs = schema.get("$defs", {})
    transform_file_defs(schema, defs)
    for k, v in defs.items():
        write_loc = get_write_loc(v)
        if write_loc:
            copied = copy.deepcopy(v)
            local_refs = find_local_refs(v)
            # relative_write_locs(copied, "../" + str(write_loc.parent) + "/")

            if local_refs:
                copied["$defs"] = {ref.removeprefix("#/$defs/"): defs[ref.removeprefix("#/$defs/")] for ref in local_refs}
            os.makedirs((dist_component_schemas / write_loc).parent, exist_ok=True)
            with open(dist_component_schemas / write_loc, 'w') as json_file:
                json.dump(copied, json_file, indent=2)


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


sitemap_groups = {
    "Machine": {
        "collapsed": True,
        "Symbolic Memory": "SymbolicMemory",
        "Similarity Memory": "SimilarityMemory",
        "File Memory": "FileMemory",
    },
    "Agents": "Agent",
    "APUs": "APU",
    "LLM Providers": "LLMUnit",
    "Tools": "LogicUnit",
}


def build_sitemap(d: dict, schema_loc: Path):
    acc = []
    for k, v in d.items():
        if isinstance(v, str):
            component_names = [n.removeprefix(f"../{k}/").removesuffix(".json") for n in os.listdir(schema_loc / v) if n != "overview.json"]
            component_names.sort()
            acc.append(dict(
                label=k,
                collapsed=True,
                items=[
                    dict(label="Overview", link=f"/docs/components/{url_safe(v)}/overview"),
                    *(dict(label=name, link=f"/docs/components/{url_safe(v)}/{url_safe(name)}") for name in component_names)
                ]
            ))
        else:
            acc.append(dict(
                label=k,
                collapsed=v.pop("collapsed", False),
                items=build_sitemap(v, schema_loc)
            ))
    return acc


def update_sitemap(astro_config_loc=EIDOLON / "webui" / "apps" / "docs" / "astro.config.mjs"):
    with open(astro_config_loc, "r") as astro_config_file:
        lines = astro_config_file.readlines()
    start_index, finish_index = None, None
    for i in range(len(lines)):
        if "### Start Components ###" in lines[i]:
            start_index = i
        if "### End Components ###" in lines[i]:
            finish_index = i
    assert start_index is not None and finish_index is not None, "Could not find start and end of components in astro.config.mjs"

    sitemap = build_sitemap(sitemap_groups, EIDOLON / "scripts" / "scripts" / "docbuilder" / "schemas")
    sitemap = json.dumps(sitemap, indent=2)
    templated = "\n".join(" " * 12 + line for line in sitemap.splitlines()) + "\n"
    with open(astro_config_loc, "w") as components_file:
        components_file.write(''.join(lines[:start_index + 1]))
        components_file.write(templated)
        components_file.write(''.join(lines[finish_index:]))


def write_md(read_loc,
             write_loc=EIDOLON / "webui" / "apps" / "docs" / "src" / "content" / "docs" / "docs" / "components"):
    shutil.rmtree(write_loc, ignore_errors=True)
    group_files = os.listdir(read_loc)
    groups = []
    for group in group_files:
        with open(read_loc / group / "overview.json", 'r') as json_file:
            groups.append(json.load(json_file))
    group_names = [g['reference_pointer']['type'] for g in groups]
    for group in groups:
        group_name = group['reference_pointer']['type']
        content = [
            "---",
            f"title: {group_name} Overview",
            f'description: "{group.get("description")}"',
            "---",
            f"Overview of the {group_name} component",
            "## Builtins"
        ]
        components = []
        for c in [c for c in os.listdir(read_loc / group_name) if c != "overview.json"]:
            with open(read_loc / group_name / c, 'r') as json_file:
                components.append(json.load(json_file))
        for component_schema in sorted(components, key=lambda c: c['reference_details']['name']):
            component_name = component_schema['reference_details']['name']
            content.append(f"* [{component_name}](/docs/components/{url_safe(group_name)}/{url_safe(component_name)}/)")
            if component_name == group['reference_pointer']['default_impl']:
                content[-1] += " (default)"

        write_astro_md_file(
            "\n".join(content),
            write_loc / url_safe(group_name) / "overview.md",
            group_names
        )

        for schema in components:
            schema = copy.deepcopy(schema)
            clean_ref_groups_for_md(schema, {g["reference_pointer"]['type']: g["reference_pointer"]['default_impl'] for g in groups})
            title = schema.get('title', schema['reference_details']['name'])
            description = f"Description of {title} component"

            with TemporaryDirectory() as tempdir:
                with open(Path(tempdir) / c, 'w') as temp_json_file:
                    json.dump(schema, temp_json_file, indent=2)
                content = generate_from_schema(Path(tempdir) / c, config=GenerationConfiguration(
                    show_breadcrumbs=False,
                    custom_template_path=str(Path(__file__).parent / "templates" / "custom" / "base.md"),
                    with_footer=False,
                ))
                write_astro_md_file(content, write_loc / url_safe(group_name) / (url_safe(schema['reference_details']['name']) + ".md"), group_names)


def write_astro_md_file(content, write_file_loc, group_names: List[str]):
    for name in group_names:
        replacement = f"[Reference[{name}]](/docs/components/{url_safe(name)}/overview)"
        content = content.replace(f"Reference[{name}]", replacement)
        content = content.replace(f"`{replacement}`", f"[`Reference[{name}]`](/docs/components/{url_safe(name)}/overview)")

    os.makedirs(os.path.dirname(write_file_loc), exist_ok=True)

    with open(write_file_loc, 'w') as md_file:
        md_file.write(content)


def template(template_file, **kwargs):
    with open(EIDOLON / "scripts" / "scripts" / "docbuilder" / template_file) as template:
        return Environment(undefined=StrictUndefined).from_string(template.read()).render(**kwargs)


def clean_ref_groups_for_md(schema, group_defaults, seen=None):
    seen = seen or set()
    if id(schema) in seen:
        return

    seen.add(id(schema))
    if isinstance(schema, dict):  # inline optional types for easier to read markdown
        if "anyOf" in schema and len(schema['anyOf']) == 2 and [s for s in schema['anyOf'] if len(s) == 1 and s.get("type") == "null"] and schema.get('default') is None:
            any_of = schema.pop('anyOf')
            object_type = [s for s in any_of if not (len(s) == 1 and s.get("type") == "null")][0]
            schema.update(object_type)
        if "$ref" in schema and schema["$ref"].endswith("/overview.json"):
            ref: str = schema.pop("$ref")
            group = ref.removeprefix("../").removesuffix("/overview.json")
            schema['type'] = f"Reference[{group}]"
            if 'default' not in schema:
                schema['default'] = dict(implementation=group_defaults[group])
        for v in schema.values():
            clean_ref_groups_for_md(v, group_defaults, seen)
    elif isinstance(schema, list):
        for i in schema:
            clean_ref_groups_for_md(i, group_defaults, seen)
    else:
        pass


def url_safe(name: str) -> str:
    return name.replace(" ", "_").replace(".", "_").lower()


if __name__ == "__main__":
    main()
