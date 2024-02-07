from eidolon_ai_sdk.memory.file_memory import FileMemory
from eidolon_ai_sdk.memory.semantic_memory import SymbolicMemory
from eidolon_ai_sdk.memory.similarity_memory import SimilarityMemory


class AgentMemory:
    file_memory: FileMemory
    symbolic_memory: SymbolicMemory
    similarity_memory: SimilarityMemory

    def __init__(
        self,
        file_memory: FileMemory = None,
        symbolic_memory: SymbolicMemory = None,
        similarity_memory: SimilarityMemory = None,
    ):
        self.file_memory = file_memory
        self.symbolic_memory = symbolic_memory
        self.similarity_memory = similarity_memory

    def start(self):
        if self.file_memory:
            self.file_memory.start()
        if self.symbolic_memory:
            self.symbolic_memory.start()
        if self.similarity_memory:
            self.similarity_memory.start()

    def stop(self):
        if self.file_memory:
            self.file_memory.stop()
        if self.symbolic_memory:
            self.symbolic_memory.stop()
        if self.similarity_memory:
            self.similarity_memory.stop()
