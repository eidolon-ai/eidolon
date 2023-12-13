import os
import readline
from urllib.parse import urlparse

from rich.console import Console

from eidolon_cli.eidolon_cli import EidolonClient

history_file = os.path.expanduser('~/.eidolon.history')
history_file_size = 1000

client = EidolonClient()
console = Console()


commands = ["/list", "/conversation", "quit"]


def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')

readline.set_completer(completer)


def print_prompt():
    if client.server_location is None:
        location = "[gray70](disconnected)[/gray70]"
    else:
        url = urlparse(client.server_location)
        location = f"[#8a8a8a]({url.hostname}:{url.port}"
        if client.agent:
            location += f"/agents/{client.agent}"
            if client.endpoint:
                location += f"/programs/{client.endpoint}"
        location += ")[/#8a8a8a]"
    console.print(location, end="")
    console.print(" eidolon % ", end="")


async def run(endpoint: str):
    await client.set_server_location(endpoint)
    console.print(f"Connected to {endpoint}")
    current_conversation = None
    command = ""
    if readline and os.path.exists(history_file):
        readline.read_history_file(history_file)
    while command != "quit":
        if current_conversation:
            agent = await client.get_client(current_conversation[0])
            agent.schema.await_input()

        else:
            print_prompt()
            command = console.input()
            if command == "/list":
                agents_ = await client.list_agents()
                for agent in agents_:
                    agent.print_to_console(console)
            elif command.startswith("/conversation "):
                agent = command.split(" ")[1]
                current_conversation = (agent, None)
            elif command == "quit":
                console.print("Goodbye!")
            else:
                console.print("Unknown command")
        readline.set_history_length(history_file_size)
        readline.write_history_file(history_file)
