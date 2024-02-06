import json
import os.path
import re
from typing import Optional, List, Dict
from urllib.parse import urljoin

import httpx
import markdown
from httpx_sse import EventSource
from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from rich.console import Console

from eidolon_ai_cli.StreamProcessor import StreamProcessor
from eidolon_ai_cli.live_console import LiveConsole
from eidolon_ai_cli.markdown import Markdown
from eidolon_ai_cli.schema import Schema, AgentEndpoint


class EidolonClient:
    server_location: Optional[str] = None
    timeout = httpx.Timeout(5.0, read=600.0)
    agent_endpoints = None

    def __init__(self, security_headers: Dict[str, str] = None):
        self.security_headers = security_headers
        self.set_server_location("http://localhost:8080")

    def set_server_location(self, server_location: str):
        self.server_location = server_location
        with httpx.Client(timeout=self.timeout) as client:
            openapi_json = client.get(urljoin(self.server_location, "openapi.json"), headers=self.security_headers).json()

        programs_re = "^/agents/([^/]+)/programs/([^/]+)$"
        processes_re = "^/agents/([^/]+)/processes/{process_id}/actions/([^/]+)$"
        paths: List[str] = openapi_json["paths"]
        # iterate over paths and find the ones that match the regex returning a list of tuples of the form (agent, program)
        agent_endpoints = []
        for path in paths:
            programs_results = re.search(programs_re, path)
            processes_results = re.search(processes_re, path)
            if programs_results:
                name = programs_results.group(1)
                program = programs_results.group(2)
                is_program = True
            elif processes_results:
                name = processes_results.group(1)
                program = processes_results.group(2)
                is_program = False
            else:
                continue
            agent_obj = openapi_json["paths"][path]["post"]

            description = agent_obj["description"] if "description" in agent_obj else ""
            if "requestBody" not in agent_obj:
                schema = Schema(is_multipart=False, schema={"properties": {}, "type": "object", "required": []})
            else:
                schema = Schema.from_json_schema(openapi_json, agent_obj["requestBody"]["content"])

            agent_endpoints.append(
                AgentEndpoint(agent_name=name, description=description, program=program, schema=schema, is_program=is_program)
            )
        agent_endpoints.sort(key=lambda x: x.agent_name)
        self.agent_endpoints = agent_endpoints

    def get_client(self, user_agent: str, user_program: str, is_program: Optional[bool]):
        for agent in self.agent_endpoints:
            if (
                    agent.agent_name == user_agent
                    and agent.program == user_program
                    and (is_program is None or agent.is_program == is_program)
            ):
                return agent
        return None

    def send_request(self, agent, user_input, process_id, show_markdown: bool):
        with httpx.Client(timeout=self.timeout) as client:
            if agent.is_program:
                agent_url = f"/agents/{agent.agent_name}/programs/{agent.program}"
            else:
                agent_url = f"/agents/{agent.agent_name}/processes/{process_id}/actions/{agent.program}"
            if agent.schema.is_multipart:
                files = None
                data = {}

                def read_file(path: str):
                    with open(path, "rb") as f:
                        return f.read()

                for k, v in agent.schema.schema["properties"].items():
                    if v.get("type") == "string" and v.get("format") == "binary":
                        if user_input[k] and len(user_input[k]) > 0:
                            files = {k: (os.path.basename(user_input[k]), read_file(user_input[k]))}
                    elif (
                            v.get("type") == "array"
                            and v["items"].get("type") == "string"
                            and v["items"].get("format") == "binary"
                    ):
                        if user_input[k] and len(user_input[k]) > 0:
                            files = [(k, read_file(file)) for file in user_input[k]]
                    else:
                        data[k] = json.dumps(user_input[k])
                # for file_name, file in files:
                #     print("file", file_name, len(file))
                request = {"url": urljoin(self.server_location, agent_url), "data": data}
                if files:
                    request["files"] = files
            else:
                request = {"url": urljoin(self.server_location, agent_url), "json": user_input}
            headers = {**self.security_headers, "Accept": "text/event-stream"}
            with client.stream(method="POST", **request, headers=headers) as response:
                content_type = response.headers.get("content-type", "").partition(";")[0]
                status_code = response.status_code
                if status_code != 200:
                    print_formatted_text(f"Error: {str(response)}")
                    return [], None

                if "text/event-stream" in content_type:
                    sp = StreamProcessor()
                    md = Markdown(sp.generate_tokens(EventSource(response).iter_sse()))
                    console = LiveConsole()
                    console.print_live(md)
                    return sp.available_actions, sp.process_id
                else:
                    response.read()
                    response = response.json()
                    if isinstance(response["data"], str):
                        if show_markdown:
                            html = markdown.markdown(response["data"].strip())
                            print_formatted_text(HTML(html))
                        else:
                            print_formatted_text(response["data"])
                    else:
                        print_formatted_text(json.dumps(response["data"]))

                    if response["state"] == "terminated":
                        return [], None
                    else:
                        actions = response["available_actions"]
                        # else leave current_conversation as is
                        process_id = response["process_id"]
                        return actions, process_id

    def get_processes(self, agent_name):
        with httpx.Client(timeout=self.timeout) as client:
            processes_url = f"/agents/{agent_name}/processes"
            processes_obj = client.get(urljoin(self.server_location, processes_url), params={"limit": 999}, headers=self.security_headers).json()
            return processes_obj["processes"]

    def have_conversation(
            self,
            agent_name,
            actions: str | List[str],
            process_id,
            console: Console,
            start_of_conversation: bool,
            show_markdown: bool,
    ):
        session = PromptSession()
        while True:
            skip_prompt = False
            if isinstance(actions, str):
                agent = self.get_client(agent_name, actions, start_of_conversation)
                skip_prompt = True
            elif len(actions) == 1:
                agent = self.get_client(agent_name, actions[0], start_of_conversation)
                if len(agent.schema.schema["properties"]) != 0:
                    skip_prompt = True

            if not skip_prompt:
                action = ""
                valid_input = False
                if len(actions) == 1:
                    default = actions[0]
                else:
                    default = ""
                while not valid_input:
                    session.completer = WordCompleter(actions)
                    action = session.prompt(f"action [{','.join(actions)}]: ", default=default)
                    session.completer = None
                    if action in actions:
                        valid_input = True
                    else:
                        console.print("Invalid action")
                agent = self.get_client(agent_name, action, start_of_conversation)

            agentSession = PromptSession()
            user_input = agent.schema.await_input(agentSession)
            if user_input is None:
                console.print()
                break
            console.print("Sending request...", style="dim")

            actions, process_id = self.send_request(agent, user_input, process_id, show_markdown)
            start_of_conversation = False
            if len(actions) == 0:
                break
