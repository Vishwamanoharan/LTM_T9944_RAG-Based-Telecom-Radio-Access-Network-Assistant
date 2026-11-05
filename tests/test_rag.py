from rag_engine.retriever.query_processor import (
    QueryProcessor
)

from rag_engine.retriever.retriever import (
    Retriever
)

from rag_engine.retriever.source_retriever import (
    SourceRetriever
)

from rag_engine.reranker.reranker import (
    Reranker
)


def print_results(
    results,
    show_rerank_score=False
):

    for result in results:

        print()

        print(
            "Rank:",
            result["rank"]
        )

        print(
            "Score:",
            round(
                result["score"],
                4
            )
        )

        if show_rerank_score:

            print(
                "Rerank Score:",
                round(
                    result["rerank_score"],
                    4
                )
            )

        print(
            "Dataset:",
            result["dataset"]
        )

        print(
            "Source:",
            result["source"]
        )

        print(
            "Document:",
            result["document"]
        )

        text = result["text"]

        print(
            "Text:",
            text[:300].replace(
                "\n",
                " "
            )
        )


def main():

    print()
    print("=" * 70)
    print("RAG / QDRANT / RERANKING TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # QUERY PROCESSOR
    # ---------------------------------------------------------

    processor = QueryProcessor()

    query = (
        "What happens when network congestion "
        "causes high PRB utilization?"
    )

    processed = processor.process(
        query
    )

    assert processed["valid"] is True

    assert (
        processed["processed_query"]
        == query
    )

    print()
    print(
        "Query processor test passed."
    )

    # ---------------------------------------------------------
    # QDRANT RETRIEVER
    # ---------------------------------------------------------

    retriever = Retriever(
        top_k=5
    )

    info = retriever.get_collection_info()

    print()
    print("Qdrant Collection")
    print("-" * 70)

    print(
        "Collection:",
        info["collection_name"]
    )

    print(
        "Vectors:",
        info["vectors_count"]
    )

    print(
        "Dimensions:",
        info["vector_size"]
    )

    assert (
        info["collection_name"]
        == "telecom_rag"
    )

    assert (
        info["vectors_count"] > 0
    )

    assert (
        info["vector_size"] == 384
    )

    print()
    print(
        "Qdrant collection validation passed."
    )

    # ---------------------------------------------------------
    # QUERY 1
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("QUERY 1 - VECTOR RETRIEVAL")
    print("=" * 70)

    print(query)

    retrieved_results = retriever.retrieve(
        query,
        top_k=5
    )

    assert len(retrieved_results) > 0

    print()
    print(
        "Retrieved:",
        len(retrieved_results),
        "documents"
    )

    print_results(
        retrieved_results
    )

    print()
    print(
        "Vector retrieval validation passed."
    )

    # ---------------------------------------------------------
    # RERANKER
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("RERANKING")
    print("=" * 70)

    reranker = Reranker()

    reranked_results = reranker.rerank(
        query=query,
        documents=retrieved_results,
        top_k=3
    )

    assert len(reranked_results) > 0

    assert len(reranked_results) <= 3

    for result in reranked_results:

        assert (
            "rerank_score"
            in result
        )

        assert isinstance(
            result["rerank_score"],
            float
        )

    # Verify descending rerank order

    rerank_scores = [
        result["rerank_score"]
        for result in reranked_results
    ]

    assert rerank_scores == sorted(
        rerank_scores,
        reverse=True
    )

    print()
    print(
        "Reranked:",
        len(reranked_results),
        "documents"
    )

    print_results(
        reranked_results,
        show_rerank_score=True
    )

    print()
    print(
        "Reranking validation passed."
    )

    # ---------------------------------------------------------
    # QUERY 2
    # ---------------------------------------------------------

    query2 = (
        "What is the effect of low SINR "
        "on radio network performance?"
    )

    print()
    print("=" * 70)
    print("QUERY 2 - VECTOR RETRIEVAL + RERANKING")
    print("=" * 70)

    print(query2)

    retrieved_results2 = retriever.retrieve(
        query2,
        top_k=5
    )

    assert len(retrieved_results2) > 0

    print()
    print(
        "Retrieved:",
        len(retrieved_results2),
        "documents"
    )

    reranked_results2 = reranker.rerank(
        query=query2,
        documents=retrieved_results2,
        top_k=3
    )

    assert len(reranked_results2) > 0

    assert len(reranked_results2) <= 3

    print()
    print(
        "Reranked:",
        len(reranked_results2),
        "documents"
    )

    print_results(
        reranked_results2,
        show_rerank_score=True
    )

    print()
    print(
        "Query 2 reranking validation passed."
    )

    # ---------------------------------------------------------
    # SOURCE RETRIEVER
    # ---------------------------------------------------------

    source_retriever = SourceRetriever(
        retriever=retriever
    )

    source_results = source_retriever.retrieve(
        query,
        top_k=5
    )

    assert len(source_results) > 0

    sources = source_retriever.get_sources(
        source_results
    )

    assert len(sources) > 0

    print()
    print("=" * 70)
    print("SOURCE RETRIEVER")
    print("=" * 70)

    for source in sources:

        print(
            f"Rank={source['rank']} | "
            f"Score={source['score']:.4f} | "
            f"Dataset={source['dataset']} | "
            f"Document={source['document']}"
        )

    print()
    print(
        "Source retrieval validation passed."
    )

    # ---------------------------------------------------------
    # EMPTY QUERY
    # ---------------------------------------------------------

    empty_results = retriever.retrieve(
        "",
        top_k=5
    )

    assert empty_results == []

    print()
    print(
        "Empty query validation passed."
    )

    # ---------------------------------------------------------
    # EMPTY RERANKING
    # ---------------------------------------------------------

    empty_reranked = reranker.rerank(
        query=query,
        documents=[],
        top_k=3
    )

    assert empty_reranked == []

    print()
    print(
        "Empty reranking validation passed."
    )

    # ---------------------------------------------------------
    # FINAL
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "ALL RAG / QDRANT / RERANKING TESTS PASSED"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()