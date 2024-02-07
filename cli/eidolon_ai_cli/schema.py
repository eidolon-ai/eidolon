import copy
import json
import os
from dataclasses import dataclass
from typing import Dict, Any

from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.completion import Completer, PathCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import get_by_name
from prompt_toolkit.keys import Keys
from prompt_toolkit.validation import Validator
from rich.console import Console

from eidolon_ai_cli.util import rt, NumberValidator, BooleanValidator, RequiredValidator, FilePathValidator

LIGHT_GREY = "'#666666'"


class ObjInput:
    session: PromptSession

    def __init__(self, session: PromptSession):
        self.session = session
        self.multiline_bindings = KeyBindings()

        @self.multiline_bindings.add(Keys.ControlD, eager=True)
        def _(event):
            get_by_name("accept-line").call(event)

        @self.multiline_bindings.add(Keys.ControlC, eager=True)
        def _(_event):
            # get_by_name("end-of-file").call(event)
            raise KeyboardInterrupt()

    def get_input_from_obj(self, obj: Dict[str, Any], padding_level: int) -> Dict[str, Any]:
        obj_input = {}
        for k, v in obj.items():
            if isinstance(v, dict):
                required = v.get("is_required", False)
                default_value = v.get("default") or ""
                # print_formatted_text("default: " + str(default_value))
                # print_formatted_text("type: " + str(v.get("type")))
                if not v.get("type"):
                    print(json.dumps(v))

                padding_str = ' ' * padding_level

                def print_field(add_colon: bool = True) -> HTML:
                    prompt = f"{padding_str}{k}"
                    if required:
                        prompt = f"<b>{prompt}✵</b>"

                    if add_colon:
                        prompt += ": "

                    return HTML(prompt)

                def do_prompt(message: str | HTML, is_required: bool, validator: Validator = None,
                              multiline: bool = False, key_bindings: KeyBindings = None,
                              bottom_toolbar=None, completer: Completer = None, default="") -> str:
                    # super lame of the toolkit that I have to do this...
                    session = PromptSession()
                    validator = RequiredValidator(is_required, validator)

                    return session.prompt(message, validator=validator, multiline=multiline, key_bindings=key_bindings,
                                          bottom_toolbar=bottom_toolbar, default=str(default), completer=completer)

                if v.get("type") == "object":
                    if not required:
                        user_input = do_prompt(f"{padding_str}add optional object {k}?: ", True, validator=BooleanValidator())
                        if user_input == "y" or user_input == "yes" or user_input == "1" or user_input == "true":
                            obj_input[k] = self.get_input_from_obj(v["properties"], padding_level + 2)
                    else:
                        print_formatted_text(HTML(f"{padding_str}  <style fg={LIGHT_GREY}>Enter values for {k}:</style>"))
                        obj_input[k] = self.get_input_from_obj(v["properties"], padding_level + 2)
                elif v.get("type") == "array":
                    if v["items"].get("type") == "object":
                        arr_input = []
                        while do_prompt(f"{padding_str}add new object to array {k}?: ", True, validator=BooleanValidator()) == "y":
                            print_formatted_text(HTML(f"{padding_str}  <style fg={LIGHT_GREY}>Enter values for {k}:</style>"))
                            arr_input.append(self.get_input_from_obj(v["items"]["properties"], padding_level + 2))
                        obj_input[k] = arr_input
                    elif v["items"].get("type") == "string" and v["items"].get("format") == "binary":
                        files = []
                        file_prompt = print_field()
                        while True:
                            try:
                                file = do_prompt(file_prompt, is_required=required, validator=FilePathValidator(), completer=PathCompleter(expanduser=True),
                                                 bottom_toolbar=lambda: "Enter a file on each line. Ctrl-C to reject the current line and stop entering files.")
                                if file and len(file) > 0:
                                    file = os.path.expanduser(file)
                                    file = os.path.expandvars(file)
                                    file = os.path.abspath(file)
                                files.append(file)
                                file_prompt = ' ' * (len(f"{padding_str}{k}") + 2)
                            except KeyboardInterrupt:
                                break

                        obj_input[k] = files
                    else:
                        print_formatted_text(HTML(f"{padding_str}  <style fg={LIGHT_GREY}>Enter array values for {k}, each on a separate line:</style>"))
                        arr_input = do_prompt(print_field(), is_required=required, multiline=True, key_bindings=self.multiline_bindings,
                                              bottom_toolbar=lambda: "Ctrl-D or Option-Enter to submit, Ctrl-C to cancel")
                        obj_input[k] = arr_input.split("\n")
                elif v.get("type") == "string" and v.get("format") == "binary":
                    file = do_prompt(print_field(), is_required=required, validator=FilePathValidator(), completer=PathCompleter(expanduser=True))
                    if file and len(file) > 0:
                        file = os.path.expanduser(file)
                        file = os.path.expandvars(file)
                        file = os.path.abspath(file)
                    obj_input[k] = file
                else:
                    if v.get("type") == "integer":
                        obj_input[k] = int(do_prompt(print_field(), is_required=required, default=default_value, validator=NumberValidator(allow_negative=True)))
                    elif v.get("type") == "number":
                        obj_input[k] = float(
                            do_prompt(print_field(), is_required=required, default=default_value, validator=NumberValidator(allow_negative=True, allow_float=True)))
                    elif v.get("type") == "boolean":
                        user_input = do_prompt(print_field(), is_required=required, default=default_value, validator=BooleanValidator())
                        obj_input[k] = user_input == "y" or user_input == "yes" or user_input == "1" or user_input == "true"
                    elif v.get("type") == "string":
                        obj_input[k] = do_prompt(print_field(), is_required=required, multiline=True, key_bindings=self.multiline_bindings,
                                                 bottom_toolbar=lambda: "Ctrl-D or Option-Enter to submit, Ctrl-C to cancel")
                    else:
                        obj_input[k] = do_prompt(print_field(), is_required=required, default=default_value)
        return obj_input


@dataclass
class Schema:
    is_multipart: bool
    schema: Dict[str, Any]

    def await_input(self, session: PromptSession):
        try:

            input_processor = ObjInput(session)
            print_formatted_text(HTML(f"<style fg={LIGHT_GREY}>Enter input values:</style>"))
            return_obj = input_processor.get_input_from_obj(self.schema["properties"], 0)
            return return_obj
        except KeyboardInterrupt:
            return None
        except EOFError:
            return None

    def __rich_console__(self, _console: Console, _options: Console.options):
        def print_object(obj: Dict[str, Any], padding_level: int):
            for k, v in obj.items():
                if isinstance(v, dict):
                    yield rt(f"{' ' * padding_level}{k}")
                    if v.get("is_required"):
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

        yield rt("  Schema:", style="#666666")
        if self.is_multipart:
            yield rt(" multipart/form-data\n")
        else:
            yield rt(" application/json\n")

        yield from print_object(self.schema["properties"], 4)

    @classmethod
    def from_json_schema(cls, json_schema: Dict[str, Any], obj_to_process: Dict[str, Any]):
        def process_schema_obj(obj: Dict[str, Any]):
            obj = copy.deepcopy(obj)
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
                            properties[k]["is_required"] = True
                obj["properties"] = properties

                return obj
            elif obj.get("type") == "array":
                obj["items"] = process_schema_obj(obj["items"])
                return obj
            elif "allOf" in obj:
                retObj = {}
                for cond in obj["allOf"]:
                    if "type" in cond:
                        retObj["type"] = cond["type"]
                        break
                    if "$ref" in cond:
                        retObj = process_schema_obj(cond)
                        break
                if "description" in obj:
                    retObj["description"] = obj["description"]
                if "required" in obj:
                    retObj["is_required"] = obj["is_required"]
                return retObj
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
class AgentEndpoint:
    agent_name: str
    description: str
    program: str
    schema: Schema
    is_program: bool

    def __rich_console__(self, _console: Console, _options: Console.options):
        yield rt(f"{self.agent_name}/{self.program}\n", style="bold")
        if self.description:
            yield rt("      " + self.description + "\n")
