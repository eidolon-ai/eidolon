import os
import tempfile
from typing import Annotated, Type, get_origin

import typer
import yaml
from click import Choice, BadParameter
from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType
from rich import print
from rich.syntax import Syntax

from eidos.system.reference_model import Reference
from eidos.system.resources import agent_resources, AgentResource
from eidos.util.class_utils import for_name, fqn

agent_choices = Choice([a for a in agent_resources.keys() if a != "Agent"] + ["Custom"], case_sensitive=False)


def create_agent(
        name: Annotated[str, typer.Option( help="The name of the Agent", prompt=True)] = "NewAgent",
):
    kind = typer.prompt(f"What type of agent is {name}?", default="GenericAgent", type=agent_choices)
    args = dict(apiVersion="eidolon/v1")
    args["kind"] = kind if kind != "Custom" else 'Agent'

    # todo, This is just a reference, so we don't need the duplicate logic here
    if kind == "Custom":
        agent_resource = AgentResource
        fqn = typer.prompt(f"What is the fully qualified name to the implementation?", type=str, value_proc=impl_proc)
        agent_class = for_name(fqn, object)
        args["implementation"] = fqn
    else:
        agent_resource = agent_resources[kind]
        agent_class = agent_resource.clazz

    spec_type = Reference.get_spec_type(agent_class)
    if spec_type:
        if typer.confirm("Would you like to modify the spec?", default=False):
            try:
                args['spec'] = build_model(spec_type)
            except Abort:
                print(f"Aborted, leaving spec blank")
    else:
        print(f"{agent_class.__name__} does not have a spec.")

    raw_edit_loop(args, agent_resource)

    print(Syntax(yaml.safe_dump(args), "yaml"))
    save_loc = typer.prompt("Where do you want to save the resource?", default=f'{name}.yaml')
    with open(save_loc, 'w') as file:
        yaml.dump(args, file)


# todo, it would be nice to add indentation as we recurse
def build_model(model: Type[BaseModel]):
    """
    Recursively prompts user for values for a model
    """
    rtn = {}
    for field_name, field_info in model.model_fields.items():
        description = field_info.description
        default = field_info.default if not isinstance(field_info.default, PydanticUndefinedType) else None
        prompt_text = f"{field_name}" if not description else f"{field_name} ({description})"
        # todo, it is lame we need to special case references, we should upgrade spec to be typed
        try:
            if isinstance(field_info.annotation, type) and issubclass(field_info.annotation, Reference):
                print(prompt_text + ":")
                reference = build_reference(field_info)
                if reference:
                    rtn[field_name] = reference
            elif isinstance(field_info.annotation, type) and issubclass(field_info.annotation, BaseModel):
                print(f"{prompt_text} [{default or field_info.annotation}]")
                if typer.confirm(f"Would you like to modify modify the nested field?", default=False):
                    rtn[field_name] = build_model(field_info.annotation)

            else:
                # todo, we should support unions, literals, ect nicely with custom prompts
                type_ = field_info.annotation
                if get_origin(field_info.annotation) and get_origin(field_info.annotation) in [dict, list]:
                    type_ = get_origin(field_info.annotation)
                if type_ not in [dict, list]:
                    type_ = str

                user_value = typer.prompt(prompt_text, default=default, type=type_)
                if user_value != default:
                    rtn[field_name] = user_value
        except Abort:
            print(f"Aborted, accepting defaults for {field_name}")

    return raw_edit_loop(rtn, model)


def raw_edit_loop(obj, model: Type[BaseModel]):
    """
    Validates object with model and gives user chance to edit in vim. Rinse and repeat.
    :raises Abort: If user chooses to abort
    """

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        yaml.dump(obj, temp)
        while True:
            try:
                model.model_validate(obj).model_dump(exclude_defaults=True)
                break
            except ValueError as e:
                print(e)
                action = typer.prompt(
                    f"{model.__name__} validation failed.",
                    default="Edit",
                    type=Choice(["Edit", "Ignore", "Abort"], case_sensitive=False)
                )
                if action == "Ignore":
                    break
                elif action == "Edit":
                    os.system(f'vim {temp.name}')
                    with open(temp.name) as file:
                        obj = yaml.safe_load(file)
                elif action == "Abort":
                    raise Abort()
                else:
                    raise Exception(f"Unexpected choice {action}")
    return obj


class Abort(Exception):
    pass


def impl_proc(implementation: str):
    try:
        for_name(implementation, object)
        return implementation
    except ValueError as e:
        raise BadParameter(f"Unable to import {implementation}: {e}")


def build_reference(field_info):
    ref_object = {}
    default_type = field_info.annotation._default.default
    default_impl = fqn(default_type) if default_type else None
    impl_value = typer.prompt(
        "Fully qualified name of the reference:", default=default_impl, value_proc=impl_proc
    )
    if impl_value != default_impl:
        ref_object["implementation"] = impl_value
    spec_type = Reference.get_spec_type(for_name(impl_value, object))
    if spec_type:
        if spec_type and typer.confirm("Would you like to modify the spec?", default=False):
            spec = build_model(spec_type)
            if spec:
                ref_object["spec"] = spec
    return raw_edit_loop(ref_object, field_info.annotation) if ref_object else None


def main():
    typer.run(create_agent)


if __name__ == "__main__":
    main()
