import importlib.metadata
import inspect
import os
import pkgutil
import readline
import sys
import tempfile
from contextlib import contextmanager
from functools import cache
from typing import Type, get_origin

import typer
import yaml
from click import Choice, BadParameter
from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType
from rich import print as richprint
from rich.syntax import Syntax

from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources import agent_resources, AgentResource
from eidolon_ai_sdk.util.class_utils import for_name, fqn

echo = lambda text, **kwargs: typer.echo(pad(text), **kwargs)  # noqa
confirm = lambda text, **kwargs: typer.confirm(pad(text), **kwargs)  # noqa


def prompt(text, default=None, choices: list[str] = None, case_sensitive=False, **kwargs):
    def completer(text, state):
        if case_sensitive:
            options = [i for i in choices if i.startswith(text)]
        else:
            options = [i for i in choices if i.lower().startswith(text.lower())]
        return options[state] if state < len(options) else None

    if choices:
        kwargs["type"] = Choice(choices, case_sensitive=case_sensitive)
    kwargs["default"] = default
    return prompt_with_completer(text, completer, **kwargs)


def prompt_with_completer(text, completer: callable, **kwargs):
    readline.set_completer(completer)
    rtn = typer.prompt(pad(text), **kwargs)
    readline.set_completer(None)
    return rtn


@cache
def autocomplete_modules(package_name: str, substring: str):
    try:
        package = importlib.import_module(package_name)
        submodules = []
        # if we are at a module, we want all the classes within it
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            if name.startswith(substring):
                submodules.append(package_name + "." + name + ".")
        return submodules
    except ModuleNotFoundError:
        return []


@cache
def autocomplete_packages(substring: str):
    installed_packages = (dist.metadata["Name"] for dist in importlib.metadata.distributions())
    rtn = [pkg for pkg in installed_packages if pkg.startswith(substring)]
    return rtn


def fqn_completer(text, state):
    # Split the text by dots and get the last part that's being typed
    parts = text.split(".")
    packages = autocomplete_packages(parts[0])
    if len(packages) > 1:
        options = packages
    else:
        if len(parts) > 1:
            package_name = ".".join(parts[:-1])
            substring = parts[-1]
        else:
            package_name = packages[0]
            substring = ""
        if hasattr(importlib.import_module(package_name), "__path__"):
            options = autocomplete_modules(package_name, substring)
        else:
            classes = (n for n, v in inspect.getmembers(sys.modules[package_name], inspect.isclass))
            options = [package_name + "." + c for c in classes if c.startswith(substring)]
    return options[state] if state < len(options) else None


def create_agent():
    agents = [a for a in agent_resources.keys() if a != "Agent"] + ["Custom"]

    name = prompt("What is the name of the agent?", default="NewAgent")
    kind = prompt(f"What type of agent is {name}?", default="GenericAgent", choices=agents)
    args = dict(apiVersion="eidolon/v1")
    args["kind"] = kind if kind != "Custom" else "Agent"

    # todo, This is just a reference, so we don't need the duplicate logic here
    if kind == "Custom":
        agent_resource = AgentResource
        fqn_ = prompt_with_completer(
            "What is the fully qualified name to the implementation?", fqn_completer, value_proc=impl_proc
        )
        agent_class = for_name(fqn_, object)
        args["implementation"] = fqn_
    else:
        agent_resource = agent_resources[kind]
        agent_class = agent_resource.clazz

    spec_type = Reference.get_spec_type(agent_class)
    if spec_type:
        if confirm("Would you like to modify the spec?", default=False):
            try:
                with indented():
                    args["spec"] = build_model(spec_type)
            except Abort:
                echo("Aborted, leaving spec blank")
    else:
        echo(f"{agent_class.__name__} does not have a spec.")

    try:
        raw_edit_loop(args, agent_resource)
        richprint(Syntax(yaml.safe_dump(args), "yaml", padding=Indenter.depth * 2))
        save_loc = prompt("Where do you want to save the resource?", default=f"{name}.yaml")
        with open(save_loc, "w") as file:
            yaml.dump(args, file)
    except Abort:
        echo("Aborted.", color="red")


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
                echo(prompt_text + ":")
                with indented():
                    reference = build_reference(field_info)
                if reference:
                    rtn[field_name] = reference
            elif isinstance(field_info.annotation, type) and issubclass(field_info.annotation, BaseModel):
                echo(f"{prompt_text} [{default or field_info.annotation}]")
                if confirm("Would you like to modify modify the nested field?", default=False):
                    with indented():
                        rtn[field_name] = build_model(field_info.annotation)

            else:
                # todo, we should support unions, literals, ect nicely with custom prompts
                type_ = field_info.annotation
                if get_origin(field_info.annotation) and get_origin(field_info.annotation) in [dict, list]:
                    type_ = get_origin(field_info.annotation)
                if type_ not in [dict, list]:
                    type_ = str

                user_value = prompt(prompt_text, default=default, type=type_)
                if user_value != default:
                    rtn[field_name] = user_value
        except Abort:
            echo(f"Aborted, accepting defaults for {field_name}")

    return raw_edit_loop(rtn, model)


def raw_edit_loop(obj, model: Type[BaseModel]):
    """
    Validates object with model and gives user chance to edit in vim. Rinse and repeat.
    :raises Abort: If user chooses to abort
    """

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp:
        yaml.dump(obj, temp)
        while True:
            try:
                model.model_validate(obj).model_dump(exclude_defaults=True)
                break
            except ValueError as e:
                echo(str(e), color="red")
                action = prompt(
                    f"{model.__name__} validation failed.",
                    color=None,
                    default="Edit",
                    choices=["Edit", "Ignore", "Abort"],
                )
                if action == "Ignore":
                    break
                elif action == "Edit":
                    os.system(f"vim {temp.name}")
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
    impl_value = prompt_with_completer("implementation", fqn_completer, default=default_impl, value_proc=impl_proc)
    if impl_value != default_impl:
        ref_object["implementation"] = impl_value
    spec_type = Reference.get_spec_type(for_name(impl_value, object))
    if spec_type:
        if spec_type and confirm("Would you like to modify the spec?", default=False):
            with indented():
                spec = build_model(spec_type)
            if spec:
                ref_object["spec"] = spec
    return raw_edit_loop(ref_object, field_info.annotation) if ref_object else None


def main():
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.set_completer_delims(" \t\n;")
        readline.parse_and_bind("tab: complete")
    typer.run(create_agent)


if __name__ == "__main__":
    main()


class Indenter:
    depth = 0


@contextmanager
def indented():
    Indenter.depth += 1
    try:
        yield
    finally:
        Indenter.depth -= 1


def pad(text):
    return "".join("  " * Indenter.depth + line for line in text.splitlines(True))
