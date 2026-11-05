from qdrant_client import QdrantClient

from ingestion.embeddings.embedding_generator import (
    EmbeddingGenerator
)


class Retriever:

    def __init__(
        self,
        qdrant_path="vector_db/qdrant_data",
        collection_name="telecom_rag",
        top_k=5
    ):

        self.qdrant_path = qdrant_path
        self.collection_name = collection_name
        self.top_k = top_k

        self.client = QdrantClient(
            path=self.qdrant_path
        )

        self.embedding_generator = EmbeddingGenerator()

    def embed_query(self, query):

        embeddings = self.embedding_generator.generate(
            [query]
        )

        return embeddings[0]

    def retrieve(
        self,
        query,
        top_k=None
    ):

        if not query or not str(query).strip():
            return []

        if top_k is None:
            top_k = self.top_k

        query_vector = self.embed_query(
            str(query)
        )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True
        )

        documents = []

        for rank, result in enumerate(
            results.points,
            start=1
        ):

            payload = result.payload or {}

            documents.append(
                {
                    "rank": rank,
                    "score": float(result.score),
                    "text": payload.get(
                        "text",
                        ""
                    ),
                    "dataset": payload.get(
                        "dataset",
                        "UNKNOWN"
                    ),
                    "source": payload.get(
                        "source",
                        "UNKNOWN"
                    ),
                    "document": payload.get(
                        "document",
                        "UNKNOWN"
                    )
                }
            )

        return documents

    def search(
        self,
        query,
        top_k=None
    ):

        return self.retrieve(
            query,
            top_k
        )

    def get_collection_info(self):

        collection = self.client.get_collection(
            self.collection_name
        )

        return {
            "collection_name": (
                self.collection_name
            ),
            "vectors_count": (
                collection.points_count
            ),
            "vector_size": (
                collection.config.params.vectors.size
            )
        }

    def close(self):

        try:
            self.embedding_generator.close()
        except Exception as error:
            print(f"Embedding cleanup warning: {error}")

        try:
            self.client.close()
        except Exception as error:
            print(f"Qdrant cleanup warning: {error}")

        print("Retriever resources released.")