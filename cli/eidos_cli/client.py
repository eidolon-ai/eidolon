import json
import os.path
import re
from typing import Optional, List
from urllib.parse import urljoin

import httpx
from prompt_toolkit import PromptSession
from rich.console import Console
from rich.markdown import Markdown

from eidos_cli.schema import Schema, AgentEndpoint


class EidolonClient:
    server_location: Optional[str] = None
    timeout = httpx.Timeout(5.0, read=600.0)
    agent_endpoints = None

    def __init__(self):
        self.set_server_location("http://localhost:8080")

    def set_server_location(self, server_location: str):
        self.server_location = server_location
        with httpx.Client(timeout=self.timeout) as client:
            openapi_json = client.get(urljoin(self.server_location, "openapi.json")).json()

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

    def send_request(self, agent, user_input, process_id):
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
            response = client.post(**request)
            return response.status_code, response.json()

    def get_processes(self, agent_name):
        with httpx.Client(timeout=self.timeout) as client:
            processes_url = f"/agents/{agent_name}/processes"
            processes_obj = client.get(urljoin(self.server_location, processes_url), params={"limit": 999}).json()
            return processes_obj["processes"]

    def have_conversation(
            self,
            agent_name,
            actions: List[str],
            process_id,
            console: Console,
            start_of_conversation: bool,
            show_markdown: bool,
    ):
        session = PromptSession()
        while True:
            if len(actions) > 1:
                action = ""
                valid_input = False
                while not valid_input:
                    action = session.prompt(f"action [{','.join(actions)}]: ")
                    if action in actions:
                        valid_input = True
                    else:
                        console.print("Invalid action")
                agent = self.get_client(agent_name, action, start_of_conversation)
            elif len(actions) == 1:
                action = actions[0]
                agent = self.get_client(agent_name, action, start_of_conversation)
            else:
                raise Exception("No actions available")

            agentSession = PromptSession()
            user_input = agent.schema.await_input(agentSession)
            if user_input is None:
                console.print()
                break
            console.print("Sending request...", style="dim")
            status_code, response = self.send_request(agent, user_input, process_id)
            if status_code != 200:
                console.print(f"Error: {str(response)}", style="red")
            else:
                # console.print(f"{str(response)}")
                start_of_conversation = False

                if isinstance(response["data"], dict):
                    console.print_json(json.dumps(response["data"]))
                else:
                    if show_markdown:
                        md = Markdown(response["data"])
                        console.print(md)
                    else:
                        console.print(response["data"])

                if response["state"] == "terminated":
                    break
                else:
                    actions = response["available_actions"]
                    # else leave current_conversation as is
                    process_id = response["process_id"]
