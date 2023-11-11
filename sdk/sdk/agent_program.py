import yaml
from jsonschema import validate

from agent_cpu import agent_cpu_schema, AgentCPU
from agent_memory import AgentMemory, agent_memory_schema

agent_program_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "AgentProgram",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The unique name identifying the agent program, e.g., 'simple-chat'."
        },
        "descriptor": {
            "type": "object",
            "description": "Describes the configuration of the AgentProgram.",
            "properties": {
                "baseContainerType": {
                    "type": "string",
                    "description": "The base container type for the code, e.g., 'python'."
                },
                "cpuConfiguration": agent_cpu_schema,
                "memoryConfiguration": agent_memory_schema,
                "IOConfiguration": {
                    "type": "object",
                    "properties": {
                        "implementation": {
                            "type": "string",
                            "description": "The FQN name of an implementation."
                        },
                        # todo -- this likely belongs in the IOConfiguration implementation
                        "inputSchema": {
                            "$ref": "http://json-schema.org/draft-07/schema#"
                        },
                        "outputSchema": {
                            "$ref": "http://json-schema.org/draft-07/schema#"
                        }
                    },
                    "required": ["implementation"]
                }
            },
            "required": ["baseContainerType", "cpuConfiguration", "memoryConfiguration", "IOConfiguration"]
        },
    },
    "required": ["name", "descriptor"]
}


class AgentIO:
    def __init__(self, io_configuration: str):
        self.io_configuration = io_configuration

    def config(self):
        pass


class AgentProgram:
    def __init__(self, program_description: str):
        self.program_description = program_description
        self.program_descriptor = None
        self.agent_cpu = None
        self.agent_memory = None
        self.agent_io = None

    def config(self):
        try:
            self.program_descriptor = yaml.safe_load(self.program_description)
            validate(self.program_descriptor, agent_program_schema)
            self.agent_cpu = AgentCPU(self.program_descriptor['descriptor']['cpuConfiguration'])
            self.agent_cpu.config()
            self.agent_memory = AgentMemory(self.program_descriptor['descriptor']['memoryConfiguration'])
            self.agent_memory.config()
            self.agent_io = AgentIO(self.program_descriptor['descriptor']['IOConfiguration'])
            self.agent_io.config()
        except Exception as e:
            # todo -- handle exception
            pass
