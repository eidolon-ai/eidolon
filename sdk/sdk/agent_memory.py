class AgentMemory:
    def __init__(self, memory_configuration: str):
        self.memory_configuration = memory_configuration

    def config(self):
        pass


agent_memory_schema = {
    "type": "object",
    "properties": {
        "implementation": {
            "type": "string",
            "description": "The FQN name of an implementation."
        }
    },
    "required": ["implementation"]
}
