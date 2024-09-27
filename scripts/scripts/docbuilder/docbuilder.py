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

from eidolon_ai_sdk.agent.api_agent import APIAgent
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent.sql_agent.agent import SqlAgent
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.util.class_utils import fqn

EIDOLON = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def main():
    print("Generating json...")
    dist_component_schemas = EIDOLON / "scripts" / "scripts" / "docbuilder" / "schemas"

    # accumulated_schema = {"$defs": {
    #     "Agent": {
    #         "title": "Agent",
    #         "description": "Overview of Agent components",
    #         "anyOf": [],
    #         "reference_pointer": {
    #             "type": "Agent",
    #             "default_impl": "SimpleAgent",
    #         }
    #     }
    # }}
    # for agent in [SimpleAgent, RetrieverAgent, APIAgent, SqlAgent]:
    #     schema = agent.model_json_schema()
    #     schema['properties']['implementation'] = {
    #         "const": agent.__name__,
    #     }
    #     schema['reference_details'] = dict(
    #         overrides={},
    #         clz=fqn(agent),
    #         name=agent.__name__,
    #         group="Agent",
    #     )
    #     accumulated_schema["$defs"].update(schema.pop("$defs", {}))
    #     accumulated_schema["$defs"][agent.__name__] = schema
    #     accumulated_schema["$defs"]["Agent"]["anyOf"].append({"$ref": f"#/$defs/{agent.__name__}"})
    #
    # machine_schema = MachineResource.model_json_schema()
    # accumulated_schema["$defs"].update(machine_schema.pop("$defs", {}))
    #
    # print("writing json...")
    # shutil.rmtree(dist_component_schemas, ignore_errors=True)
    # write_json_schema(dist_component_schemas, accumulated_schema)

    print("writing md...")
    write_md(dist_component_schemas)

    # print("updating sitemap...")
    # update_sitemap()


def write_json_schema(dist_component_schemas, schema):
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
    for k in os.listdir(read_loc):
        try:
            with open(read_loc / k / "overview.json", 'r') as json_file:
                g = json.load(json_file)
        except FileNotFoundError:
            print(f"Skipping {k} as it has no overview.json")
            continue

        title = f"{k} Overview"
        content = ["## Builtins"]
        components = []
        for c in [c for c in os.listdir(read_loc / k) if c != "overview.json"]:
            with open(read_loc / k / c, 'r') as json_file:
                components.append(json.load(json_file))
        for component_schema in components:
            name = component_schema['reference_details']['name']
            content.append(f"* [{name}](/docs/components/{url_safe(k)}/{url_safe(name)}/)")
            if name == g['reference_pointer']['default_impl']:
                content[-1] += " (default)"

        write_astro_md_file(
            f"Overview of the {g['title']} component" + "\n" + "\n".join(content),
            g.get('description'),
            title,
            write_loc / url_safe(k) / "overview.md"
        )

        for schema in components:
            schema = copy.deepcopy(schema)
            clean_ref_groups_for_md(schema)
            title = schema.get('title', schema['reference_details']['name'])
            description = f"Description of {title} component"

            with TemporaryDirectory() as tempdir:
                with open(Path(tempdir) / c, 'w') as temp_json_file:
                    json.dump(schema, temp_json_file, indent=2)
                content = generate_from_schema(Path(tempdir) / c, config=GenerationConfiguration(
                    show_breadcrumbs=False,
                    template_name="md",
                    with_footer=False,
                ))
                content = content[(content.index(cut_after_str) + len(cut_after_str)):]
                write_astro_md_file(content, description, title, write_loc / url_safe(k) / (url_safe(schema['reference_details']['name']) + ".md"))


def write_astro_md_file(content, description, title, write_file_loc):
    os.makedirs(os.path.dirname(write_file_loc), exist_ok=True)

    md_str = template("template_component_md", title=title, description=description, content=content)
    with open(write_file_loc, 'w') as md_file:
        md_file.write(md_str)


def template(template_file, **kwargs):
    with open(EIDOLON / "scripts" / "scripts" / "docbuilder" / template_file) as template:
        return Environment(undefined=StrictUndefined).from_string(template.read()).render(**kwargs)


def clean_ref_groups_for_md(schema, seen=None):
    seen = seen or set()
    if id(schema) in seen:
        return

    seen.add(id(schema))
    if isinstance(schema, dict):  # inline optional types for easier to read markdown
        if "anyOf" in schema and len(schema['anyOf']) == 2 and [s for s in schema['anyOf'] if len(s) == 1 and s.get("type") == "null"] and schema.get('default') is None:
            any_of = schema.pop('anyOf')
            object_type = [s for s in any_of if not (len(s) == 1 and s.get("type") == "null")][0]
            schema.update(object_type)
        if "$ref" in schema and schema["$ref"].endswith("overview.json"):
            del schema["$ref"]
            schema['properties'] = dict(implementation=dict(type="string"))
            schema['additionalProperties'] = True
        for v in schema.values():
            clean_ref_groups_for_md(v, seen)
    elif isinstance(schema, list):
        for i in schema:
            clean_ref_groups_for_md(i, seen)
    else:
        pass


def url_safe(name: str) -> str:
    return name.replace(" ", "_").replace(".", "_").lower()


if __name__ == "__main__":
    main()
