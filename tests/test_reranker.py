
from rag_engine.retriever.source_retriever import (
    SourceRetriever
)

from rag_engine.reranker.reranker import (
    Reranker
)


def main():

    print("\n================================")
    print("RAG RERANKER TEST")
    print("================================")

    query = (
        "What causes high latency in a "
        "5G radio access network?"
    )

    print(f"\nQuery:")
    print(query)

    retriever = SourceRetriever()
    reranker = Reranker()

    try:

        # -------------------------------------------------
        # STEP 1: Retrieve candidates from Qdrant
        # -------------------------------------------------

        response = retriever.retrieve(
            query=query,
            top_k=5
        )

        retrieved_documents = response["results"]

        print("\n================================")
        print("INITIAL RETRIEVAL")
        print("================================")

        print(
            f"\nRetrieved documents: "
            f"{len(retrieved_documents)}"
        )

        for index, document in enumerate(
            retrieved_documents,
            start=1
        ):

            print("\n--------------------------------")
            print(f"Retrieved Result {index}")
            print("--------------------------------")

            print(
                f"Qdrant Score: "
                f"{document['score']}"
            )

            print(
                f"Dataset: "
                f"{document['dataset']}"
            )

            print(
                f"Source: "
                f"{document['source']}"
            )

            if document["document"]:
                print(
                    f"Document: "
                    f"{document['document']}"
                )

            if document["page"] is not None:
                print(
                    f"Page: "
                    f"{document['page']}"
                )

        # -------------------------------------------------
        # STEP 2: Rerank retrieved documents
        # -------------------------------------------------

        reranked_documents = reranker.rerank(
            query=query,
            documents=retrieved_documents,
            top_k=3
        )

        print("\n================================")
        print("RERANKED RESULTS")
        print("================================")

        print(
            f"\nReranked documents: "
            f"{len(reranked_documents)}"
        )

        for index, document in enumerate(
            reranked_documents,
            start=1
        ):

            print("\n--------------------------------")
            print(f"Reranked Result {index}")
            print("--------------------------------")

            print(
                f"Rerank Score: "
                f"{document['rerank_score']}"
            )

            print(
                f"Qdrant Score: "
                f"{document['score']}"
            )

            print(
                f"Dataset: "
                f"{document['dataset']}"
            )

            print(
                f"Source: "
                f"{document['source']}"
            )

            if document["document"]:
                print(
                    f"Document: "
                    f"{document['document']}"
                )

            if document["page"] is not None:
                print(
                    f"Page: "
                    f"{document['page']}"
                )

        # -------------------------------------------------
        # STEP 3: Validate reranking
        # -------------------------------------------------

        if not retrieved_documents:
            raise AssertionError(
                "Qdrant returned no documents."
            )

        if not reranked_documents:
            raise AssertionError(
                "Reranker returned no documents."
            )

        if len(reranked_documents) > 3:
            raise AssertionError(
                "Reranker returned more than top_k documents."
            )

        for document in reranked_documents:

            if "rerank_score" not in document:
                raise AssertionError(
                    "Rerank score is missing."
                )

        scores = [
            document["rerank_score"]
            for document in reranked_documents
        ]

        if scores != sorted(
            scores,
            reverse=True
        ):
            raise AssertionError(
                "Documents are not sorted "
                "by rerank score."
            )

        print("\n================================")
        print("RERANKER TEST PASSED")
        print("================================")

    finally:

        retriever.close()


if __name__ == "__main__":
    main()

