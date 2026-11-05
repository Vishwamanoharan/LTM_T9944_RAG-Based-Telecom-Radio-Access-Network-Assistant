from ingestion.embeddings.embedding_generator import (
    EmbeddingGenerator
)

from vector_db.qdrant.qdrant_client import (
    QdrantDBClient
)

from vector_db.qdrant.vector_store import (
    VectorStore
)


class QdrantSearchTest:

    def __init__(self):

        print("\n================================")
        print("INITIALIZING QDRANT SEARCH TEST")
        print("================================")

        # ---------------------------------------------
        # EMBEDDING GENERATOR
        # ---------------------------------------------

        self.embedding_generator = (
            EmbeddingGenerator()
        )

        # ---------------------------------------------
        # QDRANT CLIENT
        # ---------------------------------------------

        self.db = QdrantDBClient(
            path="vector_db/qdrant_data"
        )

        self.client = self.db.get_client()

        # ---------------------------------------------
        # VECTOR STORE
        # ---------------------------------------------

        self.vector_store = VectorStore(
            self.client,
            collection_name="telecom_rag"
        )

    # =================================================
    # COLLECTION COUNT
    # =================================================

    def verify_collection(self):

        print("\n================================")
        print("VERIFYING COLLECTION")
        print("================================")

        result = self.client.count(
            collection_name="telecom_rag"
        )

        count = result.count

        print(
            f"Total vectors: {count}"
        )

        if count != 16895:

            raise RuntimeError(
                "\nQDRANT COUNT VERIFICATION FAILED\n"
                f"Expected: 16895\n"
                f"Found: {count}"
            )

        print(
            "Collection count verification: PASSED"
        )

    # =================================================
    # SEMANTIC SEARCH
    # =================================================

    def search(self, query, limit=5):

        print("\n--------------------------------")
        print(f"QUERY: {query}")
        print("--------------------------------")

        # ---------------------------------------------
        # CREATE QUERY EMBEDDING
        # ---------------------------------------------

        query_embedding = (
            self.embedding_generator.generate(
                [query]
            )[0]
        )

        print(
            f"Query embedding dimension: "
            f"{len(query_embedding)}"
        )

        if len(query_embedding) != 384:

            raise RuntimeError(
                "Query embedding dimension "
                "is not 384."
            )

        # ---------------------------------------------
        # SEARCH QDRANT
        # ---------------------------------------------

        results = self.vector_store.search(
            query_embedding,
            limit=limit
        )

        if not results:

            raise RuntimeError(
                "Qdrant returned no results."
            )

        print(
            f"Results returned: "
            f"{len(results)}"
        )

        # ---------------------------------------------
        # DISPLAY RESULTS
        # ---------------------------------------------

        for index, result in enumerate(
            results,
            start=1
        ):

            payload = result.payload or {}

            score = result.score

            dataset = payload.get(
                "dataset",
                "UNKNOWN"
            )

            source = payload.get(
                "source",
                "UNKNOWN"
            )

            text = payload.get(
                "text",
                ""
            )

            print(
                f"\nResult {index}"
            )

            print(
                f"Score   : {score:.4f}"
            )

            print(
                f"Dataset : {dataset}"
            )

            print(
                f"Source  : {source}"
            )

            print(
                "Text    : "
                f"{text[:500]}"
            )

        return results

    # =================================================
    # RUN ALL TESTS
    # =================================================

    def run(self):

        print("\n================================")
        print("QDRANT SEMANTIC SEARCH TEST")
        print("================================")

        # ---------------------------------------------
        # TEST 1
        # ---------------------------------------------

        self.verify_collection()

        # ---------------------------------------------
        # TEST 2 - 3GPP
        # ---------------------------------------------

        self.search(
            "What is the overall architecture "
            "of the 5G NR radio access network?"
        )

        # ---------------------------------------------
        # TEST 3 - TELEQNA
        # ---------------------------------------------

        self.search(
            "What is the purpose of the "
            "Nmfaf 3da Data Management "
            "Deconfigure service operation?"
        )

        # ---------------------------------------------
        # TEST 4 - ORANBENCH
        # ---------------------------------------------

        self.search(
            "How can an O-RAN network "
            "optimize radio resource management?"
        )

        # ---------------------------------------------
        # TEST 5 - TELELOGS
        # ---------------------------------------------

        self.search(
            "What could cause high latency "
            "and poor network performance "
            "in a telecom network?"
        )

        print("\n================================")
        print("QDRANT SEARCH TEST COMPLETED")
        print("================================")

        print(
            "\nAll basic Qdrant semantic search "
            "checks completed successfully."
        )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    test = QdrantSearchTest()

    test.run()