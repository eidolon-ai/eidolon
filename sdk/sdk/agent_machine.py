import yaml
from jsonschema import validate

schema = {
}


class AgentMachine:
    def __init__(self, machine_description: str):
        self.machine_description = machine_description
        self.machine_descriptor = None

    def config(self):
        try:
            self.machine_descriptor = yaml.safe_load(self.machine_description)
            validate(self.machine_descriptor, schema)
        except Exception as e:
            # todo -- handle exception
            pass
