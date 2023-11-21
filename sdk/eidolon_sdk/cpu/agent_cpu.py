from typing import Any, Union, List, Dict

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageURLCPUMessage, ResponseHandler
from eidolon_sdk.cpu.control_unit import ControlUnit
from eidolon_sdk.cpu.logic_unit import MethodInfo


class AgentCPU:
    control_unit: ControlUnit

    tools: Dict[str, MethodInfo]

    def __init__(
            self,
            agent_memory: AgentMemory,
            control_unit: ControlUnit
    ):
        self.agent_memory = agent_memory
        self.control_unit = control_unit

    async def start(self, response_handler: ResponseHandler):
        pass

    async def stop(self):
        pass

    async def schedule_request(
            self,
            process_id: str,
            prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]],
            input_data: Dict[str, Any],
            output_format: Dict[str, Any]
    ):
        return await self.control_unit.process_request(process_id, prompts, input_data, output_format)
