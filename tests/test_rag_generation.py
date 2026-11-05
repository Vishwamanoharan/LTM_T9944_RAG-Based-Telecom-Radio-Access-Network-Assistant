from llm.inference_engine.response_generator import (
    ResponseGenerator
)


def main():

    print("\n")
    print("=" * 70)
    print("FULL RAG GENERATION TEST")
    print("=" * 70)

    query = (
        "What causes high latency in a "
        "5G radio access network?"
    )

    generator = ResponseGenerator()

    try:

        # --------------------------------------------------
        # RUN RAG PIPELINE
        # --------------------------------------------------

        result = generator.generate(
            query=query,
            retrieval_top_k=5,
            rerank_top_k=3,
            max_new_tokens=256
        )

        # --------------------------------------------------
        # PRINT FINAL ANSWER
        # --------------------------------------------------

        print("\n")
        print("=" * 70)
        print("FINAL RAG ANSWER")
        print("=" * 70)

        print(
            f"\n{result['answer']}"
        )

        # --------------------------------------------------
        # PRINT RETRIEVED DOCUMENTS
        # --------------------------------------------------

        retrieved_documents = (
            result["retrieved_documents"]
        )

        print("\n")
        print("=" * 70)
        print("QDRANT RETRIEVED DOCUMENTS")
        print("=" * 70)

        print(
            f"\nTotal retrieved: "
            f"{len(retrieved_documents)}"
        )

        for index, document in enumerate(
            retrieved_documents,
            start=1
        ):

            print("\n")
            print(
                f"Retrieved Document {index}"
            )
            print("-" * 70)

            print(
                f"Dataset: "
                f"{document.get('dataset', '')}"
            )

            print(
                f"Source: "
                f"{document.get('source', '')}"
            )

            print(
                f"Document: "
                f"{document.get('document', '')}"
            )

            print(
                f"Page: "
                f"{document.get('page', '')}"
            )

            print(
                f"Vector Score: "
                f"{document.get('score', '')}"
            )

            print("\nText:")

            print(
                document.get("text", "")
            )

        # --------------------------------------------------
        # PRINT RERANKED DOCUMENTS
        # --------------------------------------------------

        reranked_documents = (
            result["reranked_documents"]
        )

        print("\n")
        print("=" * 70)
        print("RERANKED EVIDENCE")
        print("=" * 70)

        print(
            f"\nTotal reranked: "
            f"{len(reranked_documents)}"
        )

        for index, document in enumerate(
            reranked_documents,
            start=1
        ):

            print("\n")
            print(
                f"Evidence {index}"
            )
            print("-" * 70)

            print(
                f"Dataset: "
                f"{document.get('dataset', '')}"
            )

            print(
                f"Source: "
                f"{document.get('source', '')}"
            )

            print(
                f"Document: "
                f"{document.get('document', '')}"
            )

            print(
                f"Page: "
                f"{document.get('page', '')}"
            )

            print(
                f"Vector Score: "
                f"{document.get('score', '')}"
            )

            print(
                f"Rerank Score: "
                f"{document.get('rerank_score', '')}"
            )

            print("\nText:")

            print(
                document.get("text", "")
            )

        # --------------------------------------------------
        # PRINT FINAL CONTEXT
        # --------------------------------------------------

        print("\n")
        print("=" * 70)
        print("FINAL RAG CONTEXT SENT TO QWEN")
        print("=" * 70)

        context = result.get(
            "context",
            ""
        )

        print(
            f"\nContext length: "
            f"{len(context)} characters"
        )

        print("\n")
        print(context)

        # --------------------------------------------------
        # PRINT SOURCES
        # --------------------------------------------------

        print("\n")
        print("=" * 70)
        print("RAG SOURCES")
        print("=" * 70)

        sources = result.get(
            "sources",
            []
        )

        print(
            f"\nTotal sources: "
            f"{len(sources)}"
        )

        for index, source in enumerate(
            sources,
            start=1
        ):

            print("\n")
            print(
                f"Source {index}"
            )

            print("-" * 70)

            print(
                f"Dataset: "
                f"{source.get('dataset', '')}"
            )

            print(
                f"Source: "
                f"{source.get('source', '')}"
            )

            print(
                f"Document: "
                f"{source.get('document', '')}"
            )

            print(
                f"Page: "
                f"{source.get('page', '')}"
            )

            print(
                f"Vector Score: "
                f"{source.get('score', '')}"
            )

            print(
                f"Rerank Score: "
                f"{source.get('rerank_score', '')}"
            )

        # --------------------------------------------------
        # TEST RESULT
        # --------------------------------------------------

        print("\n")
        print("=" * 70)
        print("FULL RAG GENERATION TEST PASSED")
        print("=" * 70)

    finally:

        generator.close()


if __name__ == "__main__":
    main()