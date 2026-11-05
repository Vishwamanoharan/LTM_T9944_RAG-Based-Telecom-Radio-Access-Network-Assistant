class RAGContextBuilder:

    def __init__(
        self,
        max_context_length=6000,
        max_document_length=2000
    ):
        self.max_context_length = max_context_length
        self.max_document_length = max_document_length

    def _format_document(
        self,
        document,
        index
    ):
        dataset = document.get(
            "dataset",
            ""
        )

        source = document.get(
            "source",
            ""
        )

        document_name = document.get(
            "document",
            ""
        )

        page = document.get(
            "page"
        )

        text = document.get(
            "text",
            ""
        )

        text = str(text).strip()

        if len(text) > self.max_document_length:
            text = text[
                :self.max_document_length
            ]

        lines = [
            f"[Evidence {index}]",
            f"Dataset: {dataset}",
            f"Source: {source}"
        ]

        if document_name:
            lines.append(
                f"Document: {document_name}"
            )

        if page is not None:
            lines.append(
                f"Page: {page}"
            )

        lines.append(
            f"Content:\n{text}"
        )

        return "\n".join(lines)

    def build(
        self,
        query,
        documents
    ):
        if query is None:
            raise ValueError(
                "Query cannot be None."
            )

        query = str(query).strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        if documents is None:
            documents = []

        if not documents:
            return {
                "query": query,
                "context": "",
                "sources": []
            }

        evidence_blocks = []
        sources = []

        current_length = 0

        for index, document in enumerate(
            documents,
            start=1
        ):

            block = self._format_document(
                document,
                index
            )

            block_length = len(block)

            if (
                current_length
                + block_length
                > self.max_context_length
            ):
                break

            evidence_blocks.append(block)

            sources.append({
                "index": index,
                "dataset": document.get(
                    "dataset",
                    ""
                ),
                "source": document.get(
                    "source",
                    ""
                ),
                "document": document.get(
                    "document",
                    ""
                ),
                "page": document.get(
                    "page"
                ),
                "score": document.get(
                    "score"
                ),
                "rerank_score": document.get(
                    "rerank_score"
                )
            })

            current_length += block_length

        context = "\n\n".join(
            evidence_blocks
        )

        return {
            "query": query,
            "context": context,
            "sources": sources
        }