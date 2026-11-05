
from rag_engine.reranker.relevance_scorer import (
    RelevanceScorer
)


class Reranker:

    def __init__(self):
        self.scorer = RelevanceScorer()

    def rerank(
        self,
        query,
        documents,
        top_k=3
    ):
        """
        Rerank retrieved documents using
        cross-encoder relevance scoring.
        """

        if not documents:
            return []

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        scores = self.scorer.score(
            query,
            documents
        )

        ranked_documents = []

        for document, score in zip(
            documents,
            scores
        ):

            result = document.copy()

            result["rerank_score"] = float(
                score
            )

            ranked_documents.append(
                result
            )

        ranked_documents.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return ranked_documents[:top_k]

