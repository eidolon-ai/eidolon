import json
import os
import readline
from urllib.parse import urlparse

from rich.console import Console

from eidolon_cli.client import EidolonClient

history_file = os.path.expanduser("~/.eidolon.history")
history_file_size = 1000

client = EidolonClient()
console = Console()


commands = ["/help", "/list", "/conversation", "quit"]


def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


if "libedit" in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.set_completer_delims(" \t\n;")
    readline.parse_and_bind("tab: complete")

readline.set_completer(completer)


def print_prompt():
    if client.server_location is None:
        location = "[gray70](disconnected)[/gray70]"
    else:
        url = urlparse(client.server_location)
        location = f"[#8a8a8a]({url.hostname}:{url.port})[/#8a8a8a]"
    console.print(location, end="")
    console.print(" eidolon % ", end="")


async def run(endpoint: str):
    await client.set_server_location(endpoint)
    console.print(f"Connected to {endpoint}")
    current_conversation = None
    process_id = None
    command = ""
    if readline and os.path.exists(history_file):
        readline.read_history_file(history_file)
    while command != "quit":
        if current_conversation:
            print(f"Conversation: {current_conversation}")
            agent = await client.get_client(current_conversation)
            user_input = agent.schema.await_input(console)
            if user_input is None:
                current_conversation = None
                process_id = None
                console.print()
                continue
            status_code, response = await client.send_request(agent, user_input, process_id)
            if status_code != 200:
                console.print(f"Error: {str(response)}")
            else:
                console.print(f"{str(response)}")

                if isinstance(response["data"], dict):
                    console.print_json(json.dumps(response["data"]))
                else:
                    console.print(response["data"], style="blue")

                if response["state"] == "terminated":
                    current_conversation = None
                    process_id = None
                else:
                    actions = response["available_actions"]
                    if len(actions) > 1:
                        action = ""
                        valid_input = False
                        while not valid_input:
                            console.print(f"action [{','.join(actions)}]: ", markup=False, end="")
                            action = console.input()
                            if action in actions:
                                valid_input = True
                            else:
                                console.print("Invalid action")
                    else:
                        action = actions[0]
                    current_conversation = agent.name + "/" + action
                    process_id = response["process_id"]
        else:
            print_prompt()
            command = console.input()
            if command == "/list":
                for agent in client.agent_programs:
                    if agent.is_program:
                        console.print(agent, end="")
            elif command.startswith("/conversation "):
                agent = command.split(" ")[1]
                current_conversation = agent
            elif command.startswith("/help"):
                console.print("Available commands:")
                console.print("/list - list available agents")
                console.print("/conversation [agent] - start a conversation with an agent")
            elif command == "quit":
                console.print("Goodbye!")
            else:
                console.print("Unknown command")
        readline.set_history_length(history_file_size)
        readline.write_history_file(history_file)
