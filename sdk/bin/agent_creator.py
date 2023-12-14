import os
import tempfile
from typing import Annotated

import typer
import yaml
from click import Choice
from rich import print
from rich.syntax import Syntax

from eidos.system.resources import agent_resources, AgentResource
from eidos.system.resources_base import Metadata
from eidos.util.class_utils import for_name

agent_choices = Choice([a for a in agent_resources.keys() if a != "Agent"] + ["Other"])


def create_agent(
        name: Annotated[str, typer.Option(help="The name of the Agent", prompt=True)],
):
    kind = typer.prompt(f"What type of agent is {name}?", default="GenericAgent", type=agent_choices)
    agent_class = None
    if kind == "Other":
        kind = "Agent"
        reference = AgentResource
        while agent_class is None:
            fqn = typer.prompt(f"What is the fully qualified name to the implementation?", type=str)
            try:
                agent_class = for_name(fqn, object)
            except ValueError as e:
                print(e)
    else:

        reference = agent_resources[kind]
        agent_class = getattr(reference, "clazz", None)

    modify_spec = typer.confirm("Would you like to modify the spec?", default=False)
    if modify_spec:
        print("Unsuported")
    args = dict(
        apiVersion="eidolon/v1",
        kind=kind,
        metadata=Metadata(name=name).model_dump(exclude_defaults=True),
    )

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        yaml.dump(args, temp)
        edit_loop = True
        while edit_loop:
            try:
                reference.model_validate(args).model_dump(exclude_defaults=True)
            except ValueError as e:
                print(e)
                action = typer.prompt(
                    f"Reference validation failed.",
                    default="Edit",
                    type=Choice(["Edit", "Ignore", "Abort"], case_sensitive=False)
                ).lower()
                if action == "ignore":
                    edit_loop = False
                elif action == "edit":
                    os.system(f'vim {temp.name}')
                    with open(temp.name) as file:
                        args = yaml.safe_load(file)
                else:
                    raise e

    print(Syntax(yaml.safe_dump(args), "yaml"))
    save_loc = typer.prompt("Where do you want to save the resource?", default=f'{name}.yaml')
    with open(save_loc, 'w') as file:
        yaml.dump(args, file)


def main():
    typer.run(create_agent)


if __name__ == "__main__":
    main()
