from rag_engine.retriever.source_retriever import (
    SourceRetriever
)

from rag_engine.reranker.reranker import (
    Reranker
)

from rag_engine.retriever.context_builder import (
    RAGContextBuilder
)


def main():

    print("\n================================")
    print("RAG CONTEXT BUILDER TEST")
    print("================================")

    query = (
        "What causes high latency in a "
        "5G radio access network?"
    )

    print("\nQuery:")
    print(query)

    retriever = SourceRetriever()
    reranker = Reranker()
    context_builder = RAGContextBuilder()

    try:

        # STEP 1:
        # Retrieve candidate documents
        response = retriever.retrieve(
            query=query,
            top_k=5
        )

        retrieved_documents = (
            response["results"]
        )

        print("\n================================")
        print("RETRIEVAL")
        print("================================")

        print(
            f"Retrieved documents: "
            f"{len(retrieved_documents)}"
        )

        # STEP 2:
        # Rerank candidate documents
        reranked_documents = reranker.rerank(
            query=query,
            documents=retrieved_documents,
            top_k=3
        )

        print("\n================================")
        print("RERANKING")
        print("================================")

        print(
            f"Reranked documents: "
            f"{len(reranked_documents)}"
        )

        # STEP 3:
        # Build RAG context
        result = context_builder.build(
            query=query,
            documents=reranked_documents
        )

        context = result["context"]
        sources = result["sources"]

        print("\n================================")
        print("RAG CONTEXT")
        print("================================")

        print(
            f"\nContext length: "
            f"{len(context)} characters"
        )

        print(
            f"Sources included: "
            f"{len(sources)}"
        )

        print("\n--------------------------------")
        print("CONTEXT")
        print("--------------------------------")

        print(context)

        print("\n================================")
        print("SOURCES")
        print("================================")

        for source in sources:

            print("\n--------------------------------")

            print(
                f"Evidence: "
                f"{source['index']}"
            )

            print(
                f"Dataset: "
                f"{source['dataset']}"
            )

            print(
                f"Source: "
                f"{source['source']}"
            )

            if source["document"]:
                print(
                    f"Document: "
                    f"{source['document']}"
                )

            if source["page"] is not None:
                print(
                    f"Page: "
                    f"{source['page']}"
                )

            print(
                f"Qdrant Score: "
                f"{source['score']}"
            )

            print(
                f"Rerank Score: "
                f"{source['rerank_score']}"
            )

        # STEP 4:
        # Validate
        if not retrieved_documents:
            raise AssertionError(
                "No documents retrieved."
            )

        if not reranked_documents:
            raise AssertionError(
                "No documents after reranking."
            )

        if not context.strip():
            raise AssertionError(
                "RAG context is empty."
            )

        if not sources:
            raise AssertionError(
                "No sources were included."
            )

        if len(sources) != len(
            reranked_documents
        ):
            raise AssertionError(
                "Source count does not match "
                "reranked document count."
            )

        for source in sources:

            if "dataset" not in source:
                raise AssertionError(
                    "Dataset metadata missing."
                )

            if "source" not in source:
                raise AssertionError(
                    "Source metadata missing."
                )

            if "rerank_score" not in source:
                raise AssertionError(
                    "Rerank score missing."
                )

        print("\n================================")
        print("CONTEXT BUILDER TEST PASSED")
        print("================================")

    finally:

        retriever.close()


if __name__ == "__main__":
    main()