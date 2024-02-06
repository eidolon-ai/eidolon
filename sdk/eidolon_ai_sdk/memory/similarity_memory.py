from pydantic import BaseModel

from eidolon_ai_sdk.memory.embeddings import Embedding
from eidolon_ai_sdk.memory.vector_store import VectorStore
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class SimilarityMemorySpec(BaseModel):
    embedder: AnnotatedReference[Embedding]
    vector_store: AnnotatedReference[VectorStore]


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
