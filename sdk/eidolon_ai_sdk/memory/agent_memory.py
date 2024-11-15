from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.memory.semantic_memory import SymbolicMemoryBase
from eidolon_ai_sdk.memory.similarity_memory import SimilarityMemoryImpl


class AgentMemory:
    file_memory: FileMemoryBase
    symbolic_memory: SymbolicMemoryBase
    similarity_memory: SimilarityMemoryImpl

    def __init__(
        self,
        file_memory: FileMemoryBase = None,
        symbolic_memory: SymbolicMemoryBase = None,
        similarity_memory: SimilarityMemoryImpl = None,
    ):
        self.file_memory = file_memory
        self.symbolic_memory = symbolic_memory
        self.similarity_memory = similarity_memory

    async def start(self):
        if self.file_memory:
            await self.file_memory.start()
        if self.symbolic_memory:
            await self.symbolic_memory.start()
        if self.similarity_memory:
            await self.similarity_memory.start()

    async def stop(self):
        if self.file_memory:
            await self.file_memory.stop()
        if self.symbolic_memory:
            await self.symbolic_memory.stop()
        if self.similarity_memory:
            await self.similarity_memory.stop()
