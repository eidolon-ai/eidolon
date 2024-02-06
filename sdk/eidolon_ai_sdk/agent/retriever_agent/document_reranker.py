from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Dict, List

from eidolon_ai_sdk.system.reference_model import Specable


class DocumentReranker(ABC):
    @abstractmethod
    async def rerank(self, documents: Dict[str, Dict[str, float]]) -> List[tuple[str, float]]:
        pass


class SimpleSortedReranker(DocumentReranker):
    async def rerank(self, documents: Dict[str, Dict[str, float]]) -> List[tuple[str, float]]:
        reranked_results = {}
        for docs in documents.values():
            for doc, score in docs.items():
                if doc not in reranked_results:
                    reranked_results[doc] = [score]
                else:
                    reranked_results[doc].append(score)

        # first, average the scores
        ret = [(doc, sum(scores) / len(scores)) for doc, scores in reranked_results.items()]
        # then, sort by score
        ret = sorted(ret, key=lambda x: x[1], reverse=True)

        return ret


class RAGFusionRerankerSpec(BaseModel):
    k: int = Field(default=60, description="The rerank factor.")


class RAGFusionReranker(DocumentReranker, Specable[RAGFusionRerankerSpec]):
    async def rerank(self, documents: Dict[str, Dict[str, float]]) -> List[tuple[str, float]]:
        """Rerank a list of documents.

        Args:
            documents: The map of documents to rerank. documents is a dictionary of query -> dictionary "doc_id" -> "score".

        Returns:
            The reranked documents as a list of tuples of (doc_id, score).
        """
        fused_scores = {}
        for query, docs in documents.items():
            for rank, (doc_id, score) in enumerate(sorted(docs.items(), key=lambda x: x[1], reverse=True)):
                if doc_id not in fused_scores:
                    fused_scores[doc_id] = 0
                fused_scores[doc_id] += 1 / (rank + self.spec.k)

        reranked_results = [
            (doc, score) for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        ]

        return reranked_results
