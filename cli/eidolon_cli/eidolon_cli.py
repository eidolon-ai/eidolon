import re
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Literal
from urllib.parse import urljoin

import aiohttp
from rich.console import Console


@dataclass
class Schema:
    body: Dict[str, Any]
    files: Literal['disable', 'single', 'single-optional', 'multiple']

    def await_input(self, console: Console):
        if self.files != "disable":
            pass

    @classmethod
    def from_json_schema(cls, json_schema: Dict[str, Any], obj_to_process: Dict[str, Any]):
        def process_schema_obj(obj: Dict[str, Any]):
            if obj.get("$ref"):
                ref = obj["$ref"]
                # remove the #/ from the string, split it on / and follow json_schema objects until we get to the end
                ref = ref[2:]
                ref = ref.split("/")
                ref_obj = json_schema
                for ref_part in ref:
                    ref_obj = ref_obj[ref_part]

                return process_schema_obj(ref_obj)
            elif obj.get("type") == "object":
                required = obj.get("required", None)
                properties = obj.get("properties", {})
                ret_obj = {}
                if "title" in obj:
                    ret_obj["title"] = obj["title"]

                for k, v in properties.items():
                    ret_obj[k] = process_schema_obj(v)
                    if not required or k in required:
                        ret_obj[k]["required"] = True
                return ret_obj
            elif obj.get("type") == "array":
                ret_array = []
                for item in obj["items"]:
                    ret_array.append(process_schema_obj(item))
                return ret_array
            else:
                return obj

        top_level_schema = process_schema_obj(obj_to_process)
        if "body" in top_level_schema:
            file_type = "disable"
            if "file" in top_level_schema:
                files = top_level_schema["file"]
                if files.get("format") == "binary":
                    if "required" in files:
                        file_type = "single"
                    else:
                        file_type = "single-optional"
                else:
                    file_type = "multiple"
            return cls(body=top_level_schema["body"], files=file_type)
        else:
            return cls(body=top_level_schema, files="disable")


@dataclass
class AgentProgram:
    name: str
    description: str
    program: str
    schema: Schema

    def print_to_console(self, console: Console):
        console.print(f"  [bold]{self.name}/{self.program}[/bold]")
        console.print("      " + self.description, style="#949494")
        console.print("    Schema:")
        if self.schema.files != "disable":
            file_type = self.schema.files
            if file_type == "single-optional":
                console.print(f"      file: single")
            else:
                console.print(f"      file", end="")
                console.print("(required)", style="#bcbcbc", end="")
                console.print(": {self.schema.files}")
        def print_object(obj: Dict[str, Any], padding_level: int):
            for k, v in obj.items():
                if isinstance(v, dict) and v.get("title"):
                    console.print(f"{' ' * padding_level}{k}", end="")
                    if v.get("required"):
                        console.print("(required)", style="#bcbcbc", end="")
                    console.print(": ", end="")
                    if isinstance(v, dict) and not v.get("type"):
                        console.print()
                        print_object(v, padding_level + 2)
                    elif isinstance(v, list):
                        if len(v) > 1 and isinstance(v[0], dict):
                            console.print("[")
                            for item in v:
                                print_object(item, padding_level + 2)
                            console.print("]")
                    else:
                        console.print(v["type"])

        print_object(self.schema.body, 6)


class EidolonClient:
    openapi_json: Optional[Dict[str, Any]] = None
    server_location: Optional[str] = None
    agent: Optional[str] = None
    endpoint: Optional[str] = None

    async def set_server_location(self, server_location: str):
        self.server_location = server_location
        self.openapi_json = None
        await self.connect()

    async def connect(self):
        if not self.openapi_json:
            async with aiohttp.ClientSession() as session:
                print(self.server_location)
                async with session.get(urljoin(self.server_location, "openapi.json")) as resp:
                    self.openapi_json = await resp.json()

    async def list_agents(self):
        await self.connect()
        regex = '^/agents/([^/]+)/programs/([^/]+)$'
        paths: List[str] = self.openapi_json['paths']
        # iterate over paths and find the ones that match the regex returning a list of tuples of the form (agent, program)
        agents = []
        for path in paths:
            searchResults = re.search(regex, path)
            if searchResults:
                agent_obj = self.openapi_json['paths'][path]['post']
                description = agent_obj['description']
                content = agent_obj['requestBody']['content']
                if 'application/json' in content:
                    schema = Schema.from_json_schema(self.openapi_json, content['application/json']['schema'])
                else:
                    schema = Schema.from_json_schema(self.openapi_json, content['multipart/form-data']['schema'])

                agents.append(AgentProgram(name=searchResults.group(1), description=description, program=searchResults.group(2), schema=schema))

        return agents

    async def get_client(self, agent_str: str):
        agent, program = agent_str.split("/")
        agents = await self.list_agents()
        for agent in agents:
            if agent.name == agent and agent.program == program:
                return agent
        return None
