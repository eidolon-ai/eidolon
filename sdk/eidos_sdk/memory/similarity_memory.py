from pydantic import BaseModel, model_validator

from eidos_sdk.memory.embeddings import Embedding
from eidos_sdk.memory.vector_store import VectorStore
from eidos_sdk.system.reference_model import Specable, Reference


class SimilarityMemorySpec(BaseModel):
    embedder: Reference[Embedding] = Reference(implementation="eidos_sdk.memory.embeddings.NoopEmbedding")
    vector_store: Reference[VectorStore] = Reference(implementation="eidos_sdk.memory.noop_memory.NoopVectorStore")


class SimilarityMemory(Specable[SimilarityMemorySpec]):
    embedder: Embedding
    vector_store: VectorStore

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.embedder = self.spec.embedder.instantiate()
        self.vector_store = self.spec.vector_store.instantiate()

    def start(self):
        self.embedder.start()
        self.vector_store.start()

    def stop(self):
        self.embedder.stop()
        self.vector_store.stop()
