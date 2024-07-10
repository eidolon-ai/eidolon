import copy
import json
import os
import shutil
import textwrap
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Optional, Dict, Self

import jsonref
from jinja2 import Environment, StrictUndefined
from json_schema_for_humans.generate import generate_from_schema, generate_schemas_doc
from json_schema_for_humans.generation_configuration import GenerationConfiguration
from json_schema_for_humans.schema.schema_importer import get_schemas_to_render
from json_schema_for_humans.template_renderer import TemplateRenderer
from pydantic import BaseModel, model_validator

from eidolon_ai_sdk.agent.doc_manager.document_manager import DocumentManager
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent_os_interfaces import SimilarityMemory, SymbolicMemory
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMModel
from eidolon_ai_sdk.apu.logic_unit import LogicUnit
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.system.kernel import AgentOSKernel
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import for_name


class Group(BaseModel):
    base: type | str
    components: list[tuple[str, type, dict]] = []
    description: str = None
    document_in_sidebar: bool = True
    root: Optional[tuple[str, type, dict]] = None

    def sort_components(self):
        self.components = sorted(self.components, key=lambda x: x[0])

    @model_validator(mode='after')
    def update_description(self) -> Self:
        if not self.description:
            if isinstance(self.base, type) and self.base.__doc__:
                self.description = textwrap.dedent(self.base.__doc__)
            elif isinstance(self.base, type):
                self.description = f"Overview of {self.base.__name__} components"
            else:
                self.description = f"Overview of {self.base} components"
        return self

    def get_components(self):
        self.sort_components()
        return [*([self.root] if self.root else []), *self.components]


components_to_load: list[Group] = [
    Group(base=SymbolicMemory),
    Group(base=SimilarityMemory),
    Group(base=FileMemoryBase),
    Group(base="Agents", default="SimpleAgent", components=[
        ("SimpleAgent", SimpleAgent, {}),
        ("RetrieverAgent", RetrieverAgent, {}),
    ]),
    Group(base=APU),
    Group(base=LLMUnit),
    Group(base=LLMModel),
    Group(base=LogicUnit),
    Group(base=DocumentManager),
    Group(base=DocumentLoader),
]
groups: Dict[str, Group] = {g.base if isinstance(g.base, str) else g.base.__name__: g for g in components_to_load}
EIDOLON = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def main():
    print("Generating docs...")
    dist_component_schemas = EIDOLON / "scripts" / "scripts" / "docbuilder" / "schemas"
    shutil.rmtree(dist_component_schemas, ignore_errors=True)
    generate_groups()
    generate_json(dist_component_schemas)
    write_md(dist_component_schemas)
    update_sitemap()
    print("Done")


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
        description = f"Overview of {k} components"
        content = ["## Builtins"]
        for name, _, _ in g.get_components():
            content.append(f"* [{name}](/docs/components/{url_safe(k)}/{url_safe(name)}/)")
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
        content = content.replace(f"file:../{name}/overview.json",
                                  f"[{name}](/docs/components/{url_safe(name)}/overview)")
    os.makedirs(os.path.dirname(write_file_loc), exist_ok=True)

    md_str = template("template_component_md", title=title, description=description, content=content)
    with open(write_file_loc, 'w') as md_file:
        md_file.write(md_str)


def template(template_file, **kwargs):
    with open(EIDOLON / "scripts" / "scripts" / "docbuilder" / template_file) as template:
        return Environment(undefined=StrictUndefined).from_string(template.read()).render(**kwargs)


def generate_groups():
    # Get all groups. Groups are any Reference base used by registered component
    for r in AgentOSKernel.get_resources(ReferenceResource).values():
        overrides = Reference[object, r.metadata.name]._transform(r.spec)
        pointer = overrides.pop("implementation")
        clz = for_name(pointer, object)
        spec: Optional[BaseModel] = Reference.get_spec_type(clz)
        if spec:
            for vv in spec.model_fields.values():
                v = vv.annotation
                if hasattr(v, "_bound") and v._bound.__name__ not in groups:
                    groups[v._bound.__name__] = Group(base=v._bound, document_in_sidebar=False)

    # check all components to see which group they are in and add them to the group
    for r in AgentOSKernel.get_resources(ReferenceResource).values():
        key = r.metadata.name
        overrides = Reference[object, key]._transform(r.spec)
        pointer = overrides.pop("implementation")
        clz = for_name(pointer, object)
        for group_key, group in groups.items():
            if key == group_key:
                group.root = (key, clz, overrides)
            elif not isinstance(group.base, str) and group != object and issubclass(clz, group.base):
                group.components.append((key, clz, overrides))


def generate_json(write_base):
    for key, group in groups.items():
        write_loc = write_base / key
        os.makedirs(write_loc, exist_ok=True)

        base_json = {
            "title": key,
            "description": group.description,
            "anyOf": [{"$ref": f"file:./{name}.json"} for name, _, _ in group.get_components()],
            "reference_group":
                {"type": key}
        }
        with open(write_loc / "overview.json", 'w') as file:
            json.dump(base_json, file, indent=2)

        for name, clz, overrides in group.get_components():
            if hasattr(clz, "model_json_schema"):
                json_schema = clz.model_json_schema()
                spec = Reference.get_spec_type(clz)
                if spec:
                    for k, v in spec.model_fields.items():
                        if v.annotation.__name__ == "_Reference" and v.default_factory:
                            schema_prop = json_schema['properties'][k]
                            if "allOf" in schema_prop:
                                if len(schema_prop["allOf"]) != 1 or len(schema_prop["allOf"][0]) != 1:
                                    raise ValueError("Expected allOf to just be a json schema templating choice made by extra json properties, but that assumption is invalid")
                                schema_prop.update(schema_prop["allOf"][0])

                            def_pointer = schema_prop['$ref'].replace("#/$defs/", "")
                            default_impl: dict = json_schema['$defs'][def_pointer]['reference_pointer']['default_impl']
                            if k not in overrides:
                                overrides[k] = dict(implementation=default_impl)

                defs = dict()
                for k, v in list(json_schema.get("$defs", {}).items()):
                    if 'reference_pointer' in v:
                        if "AnnotatedReference" in v:
                            v['default'] = v['reference_pointer']['default_impl']

                        type_ = v['reference_pointer']['type']
                        if type_ in groups:
                            defs[k] = {"$ref": f"file:../{type_}/overview.json"}
                        else:
                            defs[k] = json_schema['$defs'][k]
                            defs[k]['type'] = "object"
                        del json_schema['$defs'][k]

                json_schema = inline_refs(json_schema, defs)
                if "$defs" in json_schema and not json_schema["$defs"]:
                    del json_schema["$defs"]
                json_schema['title'] = name

                for k, v in overrides.items():
                    json_schema['properties'][k]['default'] = v
                if 'required' in json_schema:
                    json_schema['required'] = [k for k in json_schema['required'] if k not in overrides]
                    if not json_schema['required']:
                        del json_schema['required']

            else:
                json_schema = {
                    "title": name,
                    "type": "object",
                }
                if clz.__doc__:
                    json_schema["description"] = textwrap.dedent(clz.__doc__)

            json_schema.setdefault('properties', {})['implementation'] = {"const": name, "description": name}
            json_schema['properties'] = dict(implementation=json_schema['properties'].pop('implementation'),
                                             **json_schema['properties'])
            with open(write_loc / (name + ".json"), 'w') as file:
                json.dump(json_schema, file, indent=2)


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
    if isinstance(schema, dict):
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
