from pydantic import BaseModel

from eidolon_sdk.cpu.agent_io import IOUnit
from eidolon_sdk.cpu.memory_unit import MemoryUnit
from eidolon_sdk.reference_model import Reference


class CpuModel(BaseModel):
    memory_unit: Reference[MemoryUnit] = Reference[MemoryUnit](implementation='eidolon_sdk.cpu.memory_unit.MemoryUnit')
    io_unit: Reference[IOUnit] = Reference[IOUnit](implementation='eidolon_sdk.cpu.agent_io.IOUnit')
