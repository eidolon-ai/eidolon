#!/usr/bin/env python3
# coding=utf-8
"""A simple example demonstrating how to use Argparse to support subcommands.


This example shows an easy way for a single command to have many subcommands, each of which takes different arguments
and provides separate contextual help.
"""
import argparse
from typing import List, Dict, Optional, Iterable, Any

import cmd2
from cmd2 import style, Fg, Bg, utils
from cmd2.argparse_custom import ChoicesProviderFunc, CompleterFunc
from rich.console import Console

from eidos_cli.client import EidolonClient


class SubcommandsExample(cmd2.Cmd):
    CUSTOM_CATEGORY = "Eidolon CLI"
    markdown = True

    """
    Example cmd2 application where we a base command which has a couple subcommands
    and the "sport" subcommand has tab completion enabled.
    """

    def __init__(self):
        super().__init__(
            multiline_commands=["echo"],
            persistent_history_file="eidolon_history.dat",
            # startup_script='scripts/startup.txt',
            include_ipy=False,
        )
        del cmd2.Cmd.do_py  # disable the "py" command
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_ipy
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_shortcuts

        self.console = Console()
        # readline.parse_and_bind("Shift-Enter: #-#-#\n")

        self.intro = style(
            "Eidolon command line tool. Type help for the list of commands.", fg=Fg.RED, bg=Bg.WHITE, bold=True
        )

        # Allow access to your application in py and ipy via self
        self.self_in_py = False

        # Set the default category name
        self.default_category = "Builtin Tools"

        self.client = EidolonClient()

    def read_input(
        self,
        prompt: str,
        *,
        history: Optional[List[str]] = None,
        completion_mode: utils.CompletionMode = utils.CompletionMode.NONE,
        preserve_quotes: bool = False,
        choices: Optional[Iterable[Any]] = None,
        choices_provider: Optional[ChoicesProviderFunc] = None,
        completer: Optional[CompleterFunc] = None,
        parser: Optional[argparse.ArgumentParser] = None,
    ) -> str:
        try:
            return super().read_input(
                prompt,
                history=history,
                completion_mode=completion_mode,
                preserve_quotes=preserve_quotes,
                choices=choices,
                choices_provider=choices_provider,
                completer=completer,
                parser=parser,
            )
        except KeyboardInterrupt:
            return "eof"

    def endpoints_provider(self) -> List[str]:
        """A choices provider is useful when the choice list is based on instance data of your application"""
        names = []
        for agent in self.client.agent_programs:
            name = f"{agent.name}/{agent.program}"
            names.append(name)

        return list(set(names))

    def programs_provider(self) -> List[str]:
        """A choices provider is useful when the choice list is based on instance data of your application"""
        return [f"{agent.name}/{agent.program}" for agent in self.client.agent_programs if agent.is_program]

    info_parser = cmd2.Cmd2ArgumentParser()
    info_arg = info_parser.add_argument(
        "endpoint", help="Enter the name of the endpoint", choices_provider=endpoints_provider, nargs="?"
    )

    @cmd2.with_category(CUSTOM_CATEGORY)
    @cmd2.with_argparser(info_parser)
    def do_info(self, arg):
        """Show information about agents endpoints"""
        if not arg.endpoint or len(arg.endpoint) == 0:
            for agent in self.client.agent_programs:
                self.console.print(agent)
        else:
            agent = self.client.get_client(arg.endpoint, None)
            self.console.print(agent)
            self.console.print(agent.schema)

    start_parser = cmd2.Cmd2ArgumentParser()
    start_arg = start_parser.add_argument(
        "endpoint", help="Enter the name of the endpoint", choices_provider=programs_provider
    )

    @cmd2.with_category(CUSTOM_CATEGORY)
    @cmd2.with_argparser(start_parser)
    def do_start(self, arg):
        """Start a process with an agent"""
        agent = self.client.get_client(arg.endpoint, is_program=True)
        process_id = None
        self.client.have_conversation(agent.name, [agent.program], process_id, self.console, True, self.markdown)

    def agent_provider(self) -> List[str]:
        """A choices provider is useful when the choice list is based on instance data of your application"""
        agents = [agent.name for agent in self.client.agent_programs]
        # now deduplicate the list
        agent_names = list(set(agents))
        agent_names.sort(reverse=True)
        return agent_names

    def agent_process_id_provider(self, arg_tokens: Dict[str, List[str]]) -> List[str]:
        """A choices provider is useful when the choice list is based on instance data of your application"""
        processes = self.client.get_processes(arg_tokens["agent"][0])
        # now we just want the processes in the "idle" state and just the process id
        process_ids = [process["process_id"] for process in processes if process["state"] != "terminated"]
        return process_ids

    resume_parser = cmd2.Cmd2ArgumentParser()
    resume_arg = resume_parser.add_argument("agent", help="Enter the name of the agent", choices_provider=agent_provider)
    resume_parser.add_argument("process_id", help="Enter the process id", choices_provider=agent_process_id_provider)

    @cmd2.with_category(CUSTOM_CATEGORY)
    @cmd2.with_argparser(resume_parser)
    def do_resume(self, arg):
        """Resume a process with an agent"""
        agent_name = arg.agent
        processes = self.client.get_processes(agent_name)
        # find the process by process_id
        process = next(process for process in processes if process["process_id"] == arg.process_id)
        if not process:
            self.console.print("Invalid process id")
            return

        self.client.have_conversation(
            agent_name, process["available_actions"], arg.process_id, self.console, False, self.markdown
        )

    def do_markdown(self, arg):
        """
        Toggle markdown rendering of output
        """
        self.markdown = not self.markdown
        self.console.print(f"Markdown rendering is now {'on' if self.markdown else 'off'}")
