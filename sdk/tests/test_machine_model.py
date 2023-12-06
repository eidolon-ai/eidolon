import yaml

from eidos.system.resource_models import MachineModel


def test_can_parse_hello_world():
    with open("../../examples/hello_world/machine_config.yaml", 'r') as file:
        file_contents = file.read()
        yaml_content = yaml.safe_load(file_contents)
        MachineModel(**yaml_content)
