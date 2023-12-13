import json
import os.path
import re
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin

import aiohttp
import httpx
from rich.console import Console

from eidolon_cli.util import rt


class ObjInput:
    console: Console

    def __init__(self, console: Console):
        self.console = console

    def _verify_files(self, user_input: str):
        # split the string on commas, but not commas inside of quotes
        # https://stackoverflow.com/questions/2785755/how-to-split-but-ignore-separators-in-quoted-strings-in-python
        files = re.findall(r'(?:[^,"]|"(?:\\.|[^"])*")+', user_input)
        # verify the files exist and are files
        for file in files:
            if not os.path.isfile(file):
                raise ValueError(f"File {file} does not exist")

        return files

    def print_field(self, padding: int, name: str, default: Optional[str], required: bool):
        prompt = f"{' ' * padding}{name}"
        if required:
            prompt += "*"
        if default:
            prompt += f" [{default}]"

        prompt += ": "
        self.console.print(prompt, end="")

    def get_file_input(self, name: str, required: bool, multiple: bool, padding_level: int) -> Union[Optional[str], List[str]]:
        if multiple:
            default = "[file path, file path, ...]"
        else:
            default = "[file path]"
        self.console.print(f"{' ' * padding_level}{name}{'*' if required else ''} {default}: ", end="")
        user_files = self.console.input()
        user_files = self._verify_files(user_files)

        if not required and user_files == "":
            user_files = None
        return user_files

    def get_input_from_obj(self, obj: Dict[str, Any], padding_level: int) -> Dict[str, Any]:
        obj_input = {}
        for k, v in obj.items():
            if isinstance(v, dict):
                if v.get("type") == "object":
                    self.print_field(padding_level, k, v.get("default"), v.get("required", False))
                    obj_input[k] = self.get_input_from_obj(v["properties"], padding_level + 2)
                elif v.get("type") == "array":
                    self.print_field(padding_level, k, v.get("default"), v.get("required", False))
                    if v["items"].get("type") == "object":
                        arr_input = []
                        self.console.print(f"{' ' * padding_level}add item? (y/n): ", end="")
                        while self.console.input() == "y":
                            arr_input.append(self.get_input_from_obj(v["items"]["properties"], padding_level + 2))
                            self.console.print(f"{' ' * padding_level}add item? (y/n): ", end="")
                        obj_input[k] = arr_input
                    elif v["items"].get("type") == "string" and v["items"].get("format") == "binary":
                        obj_input[k] = self.get_file_input(k, v["items"].get("required", False), True, padding_level)
                    else:
                        arr_input = self.console.input()
                        obj_input[k] = json.loads(arr_input)
                elif v.get("type") == "string" and v.get("format") == "binary":
                    obj_input[k] = self.get_file_input(k, v.get("required", False), False, padding_level)
                else:
                    self.print_field(padding_level, k, v.get("default"), v.get("required", False))
                    obj_input[k] = self.console.input()
        return obj_input


@dataclass
class Schema:
    is_multipart: bool
    schema: Dict[str, Any]

    def await_input(self, console: Console):
        try:
            input_processor = ObjInput(console)
            return_obj = input_processor.get_input_from_obj(self.schema["properties"], 2)
            return return_obj
        except KeyboardInterrupt:
            return None
        except EOFError:
            return None

    def __rich_console__(self, console: Console, options: Console.options):
        def print_object(obj: Dict[str, Any], padding_level: int):
            for k, v in obj.items():
                if isinstance(v, dict):
                    yield rt(f"{' ' * padding_level}{k}")
                    if v.get("required"):
                        yield rt("(required)", style="#bcbcbc")
                    yield rt(": ")
                    if v.get("type") == "object":
                        yield rt("\n")
                        yield from print_object(v["properties"], padding_level + 2)
                    elif v.get("type") == "array":
                        if v["items"].get("type") == "object":
                            yield rt("[\n")
                            for item in v:
                                yield from print_object(item, padding_level + 2)
                            yield rt("]\n")
                        elif v["items"].get("type") == "string" and v["items"].get("format") == "binary":
                            yield rt("[file]\n")
                        else:
                            yield rt(f'[{v["items"]["type"]}]\n')
                    elif v.get("type") == "string" and v.get("format") == "binary":
                        yield rt("file\n")
                    else:
                        if "type" not in v:
                            print(str(obj))
                        yield rt(v["type"] + "\n")

        yield rt(f"  Schema:", style="#666666")
        if self.is_multipart:
            yield rt(" multipart/form-data\n")
        else:
            yield rt(" application/json\n")

        yield from print_object(self.schema["properties"], 4)

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
                for k, v in properties.items():
                    if isinstance(v, dict):
                        properties[k] = process_schema_obj(v)
                        if not required or k in required:
                            properties[k]["required"] = True
                obj["properties"] = properties
                return obj
            elif obj.get("type") == "array":
                obj["items"] = process_schema_obj(obj["items"])
                return obj
            else:
                return obj

        if "application/json" in obj_to_process:
            content = obj_to_process["application/json"]["schema"]
            is_multipart = False
        elif "multipart/form-data" in obj_to_process:
            content = obj_to_process["multipart/form-data"]["schema"]
            is_multipart = True
        else:
            raise ValueError("Invalid schema")

        top_level_schema = process_schema_obj(content)
        return cls(is_multipart, top_level_schema)


@dataclass
class AgentProgram:
    name: str
    description: str
    program: str
    schema: Schema

    def __rich_console__(self, console: Console, options: Console.options):
        yield rt(f"{self.name}/{self.program}\n", style="bold")
        if self.description:
            yield rt("      " + self.description + "\n")
        yield self.schema
        yield rt("\n")


class EidolonClient:
    server_location: Optional[str] = None
    timeout = httpx.Timeout(5.0, read=600.0)
    agents = None

    async def set_server_location(self, server_location: str):
        self.server_location = server_location
        async with aiohttp.ClientSession() as session:
            async with session.get(urljoin(self.server_location, "openapi.json")) as resp:
                openapi_json = await resp.json()

        regex = "^/agents/([^/]+)/programs/([^/]+)$"
        paths: List[str] = openapi_json["paths"]
        # iterate over paths and find the ones that match the regex returning a list of tuples of the form (agent, program)
        agents = []
        for path in paths:
            searchResults = re.search(regex, path)
            if searchResults:
                agent_obj = openapi_json["paths"][path]["post"]
                description = agent_obj["description"] if "description" in agent_obj else ""
                if "requestBody" not in agent_obj:
                    schema = Schema(is_multipart=False, schema={"properties": {}, "type": "object", "required": []})
                else:
                    content = agent_obj["requestBody"]["content"]
                    schema = Schema.from_json_schema(openapi_json, content)

                agents.append(
                    AgentProgram(
                        name=searchResults.group(1),
                        description=description,
                        program=searchResults.group(2),
                        schema=schema,
                    )
                )

        self.agents = agents

    async def get_client(self, agent_str: str):
        user_agent, user_program = agent_str.strip().split("/")

        for agent in self.agents:
            if agent.name == user_agent and agent.program == user_program:
                return agent
        return None

    async def send_request(self, agent, user_input):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if agent.schema.is_multipart:
                files = []
                data = {}

                def read_file(path: str):
                    with open(path, "rb") as f:
                        return f.read()

                for k, v in agent.schema.schema["properties"].items():
                    if v.get("type") == "string" and v.get("format") == "binary":
                        files.append((os.path.basename(user_input[k][0]), read_file(user_input[k][0])))
                    elif v.get("type") == "array" and v["items"].get("type") == "string" and v["items"].get("format") == "binary":
                        for file in user_input[k]:
                            files.append(((os.path.basename(file)), read_file(file)))
                    else:
                        data[k] = json.dumps(user_input[k])
                response = await client.post(
                    urljoin(self.server_location, f"/agents/{agent.name}/programs/{agent.program}"),
                    files=files,
                    data=data
                )
                return response.status_code, response.json()
            else:
                response = await client.post(
                    urljoin(self.server_location, f"/agents/{agent.name}/programs/{agent.program}"),
                    json=user_input,
                )
                return response.status_code, response.json()
