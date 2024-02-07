from typing import Iterable, Dict, Callable, Optional

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.completion import NestedCompleter, CompleteEvent, Completion, WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.validation import Validator, ValidationError
from pygments.lexer import RegexLexer
from pygments.token import Generic, Name, Text, String, Keyword
from rich.console import Console

from eidolon_ai_cli.client import EidolonClient
from eidolon_ai_cli.security import OAuth2CLI
from eidolon_ai_cli.util import VarExpandingFileHistory


class CommandLexer(RegexLexer):
    tokens = {
        'root': [
            (r'[^\s]+', Keyword, 'agent'),
        ],
        'agent': [
            (r'[^\s]+', Name.Attribute, 'part'),
        ],
        'part': [
            (r'[^\s]+$', String),
        ]
    }


class ProcessIdCompleter(WordCompleter):
    def __init__(self, client: EidolonClient, agent_name: str, ignore_case=True, **kwargs):
        super().__init__(words=[], **kwargs)
        self.client = client
        self.agent_name = agent_name
        self.process_info = None
        self.ignore_case = ignore_case

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        if not self.process_info:
            self.process_info = self.client.get_processes(self.agent_name)
            self.words = [process["process_id"] for process in self.process_info]
        return super().get_completions(document, complete_event)


class CommandValidator(Validator):
    def __init__(self, validators: Dict[str, Callable[[str, int], None]]):
        self.validators = validators

    def validate(self, document: Document) -> None:
        text = document.text
        commands = ', '.join(self.validators.keys())
        if not text:
            raise ValidationError(message=f"Illegal command. Must be one of: {commands}", cursor_position=len(text))
        command = text.split()[0]
        if command not in self.validators:
            raise ValidationError(message=f"Illegal command. Must be one of: {commands}", cursor_position=len(text))

        validator = self.validators[command]
        if validator:
            command_len = len(command) + 1
            validator(text[command_len:], command_len)
        else:
            if len(text.split()) > 1:
                raise ValidationError(message=f"Too many arguments: {text.split()[1:]}", cursor_position=len(text))


class EidolonCLI:
    def __init__(self, security: Optional[OAuth2CLI]):
        if security:
            token = security.get_token()
            security_headers = {"Authorization": f"Bearer {token}"}
        else:
            security_headers = {}
        self.client = EidolonClient(security_headers)
        endpoints = self.client.agent_endpoints
        self.endpoints_by_agent = {}
        self.programs_by_agent = {}
        self.markdown = True
        self.console = Console()

        agents = {}
        for endpoint in endpoints:
            if endpoint.agent_name not in self.endpoints_by_agent:
                self.endpoints_by_agent[endpoint.agent_name] = {}
            self.endpoints_by_agent[endpoint.agent_name][endpoint.program] = None
            if endpoint.is_program and endpoint.agent_name not in self.programs_by_agent:
                self.programs_by_agent[endpoint.agent_name] = {}
            self.programs_by_agent[endpoint.agent_name][endpoint.program] = None
            if endpoint.agent_name not in agents:
                agents[endpoint.agent_name] = ProcessIdCompleter(self.client, endpoint.agent_name)

        self.completer = NestedCompleter.from_nested_dict({
            'info': self.endpoints_by_agent,
            'start': self.programs_by_agent,
            'resume': agents,
            'markdown': None,
            'exit': None,
        })

        self.validators = {
            'info': self.validate_info,
            'start': self.validate_start,
            'resume': self.validate_resume,
            'markdown': None,
            'exit': None,
        }

    def validate_info(self, command: str, start_pos: int):
        args = command.split()
        if len(args) == 0:
            return
        else:
            agent = args[0]
            if agent not in self.endpoints_by_agent:
                raise ValidationError(message=f"Unknown agent: {agent}", cursor_position=start_pos)
            if len(args) > 1:
                program = args[1]
                if program not in self.endpoints_by_agent[agent]:
                    raise ValidationError(message=f"Unknown endpoint: {program}", cursor_position=start_pos + len(agent) + 1)
                if len(args) > 2:
                    raise ValidationError(message=f"Too many arguments: {args[2:]}", cursor_position=start_pos + len(agent) + len(program) + 2)
            else:
                raise ValidationError(message="Missing endpoint", cursor_position=start_pos + len(agent) + 1)

    def validate_start(self, command: str, start_pos: int):
        args = command.split()
        if len(args) == 0:
            return
        else:
            agent = args[0]
            if agent not in self.programs_by_agent:
                raise ValidationError(message=f"Unknown agent: {agent}", cursor_position=start_pos)
            if len(args) > 1:
                program = args[1]
                if program not in self.programs_by_agent[agent]:
                    raise ValidationError(message=f"Unknown program: {program}", cursor_position=start_pos + len(agent) + 1)
                if len(args) > 2:
                    raise ValidationError(message=f"Too many arguments: {args[2:]}", cursor_position=start_pos + len(agent) + len(program) + 2)
            else:
                raise ValidationError(message="Missing program", cursor_position=start_pos + len(agent) + 1)

    def validate_resume(self, command: str, start_pos: int):
        args = command.split()
        if len(args) == 0:
            return
        else:
            agent = args[0]
            if agent not in self.programs_by_agent:
                raise ValidationError(message=f"Unknown agent: {agent}", cursor_position=start_pos)
            if len(args) > 1:
                pid = args[1]
                process_info = self.client.get_processes(agent)
                if pid not in [process["process_id"] for process in process_info]:
                    raise ValidationError(message=f"Unknown process: {pid}", cursor_position=start_pos + len(agent) + 1)
                if len(args) > 2:
                    raise ValidationError(message=f"Too many arguments: {args[2:]}", cursor_position=start_pos + len(agent) + len(pid) + 2)
            else:
                raise ValidationError(message="Missing process id", cursor_position=start_pos + len(agent) + 1)

    def do_markdown(self):
        self.markdown = not self.markdown
        print_formatted_text(PygmentsTokens([
            (Text, "Markdown is now "),
            (Keyword, "on") if self.markdown else (Generic.Error, "off"),
        ]))

    def do_info(self, endpoint):
        """Show information about agents endpoints"""
        if not endpoint or len(endpoint) == 0:
            for agent in self.client.agent_endpoints:
                self.console.print(agent)
        else:
            user_agent, user_program = endpoint.strip().split()

            agent = self.client.get_client(user_agent, user_program, None)
            self.console.print(agent)
            self.console.print(agent.schema)

    def do_start(self, endpoint: str):
        """Start a process with an agent"""
        user_agent, user_program = endpoint.strip().split()
        agent = self.client.get_client(user_agent, user_program, is_program=True)
        process_id = None
        self.client.have_conversation(agent.agent_name, agent.program, process_id, self.console, True, self.markdown)

    def do_resume(self, command: str):
        """Resume a process with an agent"""
        agent, process_id = command.strip().split()
        process_info = self.client.get_processes(agent)
        actions = [process["available_actions"] for process in process_info if process["process_id"] == process_id][0]
        self.client.have_conversation(agent, actions, process_id, self.console, False, self.markdown)

    def main(self):
        session = PromptSession(completer=self.completer, complete_while_typing=True, validator=CommandValidator(self.validators),
                                lexer=PygmentsLexer(CommandLexer), history=VarExpandingFileHistory('~/.eidolon_cli_history'))

        while True:
            try:
                text = session.prompt('> ')
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            else:
                if text == 'exit':
                    break
                elif text == 'markdown':
                    self.do_markdown()
                elif text.startswith('info'):
                    self.do_info(text[5:].strip())
                elif text.startswith('start'):
                    self.do_start(text[6:].strip())
                elif text.startswith('resume'):
                    self.do_resume(text[7:].strip())
                else:
                    print('You entered:', text)
        print('GoodBye!')
