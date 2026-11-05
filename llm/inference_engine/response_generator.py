
import gc

from rag_engine.retriever.source_retriever import SourceRetriever
from rag_engine.reranker.reranker import Reranker
from rag_engine.retriever.context_builder import RAGContextBuilder
from llm.prompt_manager.telecom_qa_prompt import TelecomQAPrompt
from llm.qwen_2_5.inference import QwenInference


class ResponseGenerator:

    def __init__(self, use_reranker=False):

        print("\nInitializing Low-Memory Telecom RAG Assistant...")

        self.use_reranker = use_reranker

        self.retriever = SourceRetriever()
        self.reranker = None
        self.context_builder = RAGContextBuilder()
        self.prompt_manager = TelecomQAPrompt()
        self.llm = None

        print("Low-memory RAG Assistant initialized.")

    def generate(
        self,
        query,
        retrieval_top_k=5,
        rerank_top_k=3,
        max_new_tokens=128
    ):

        if query is None or not str(query).strip():
            raise ValueError("Query cannot be empty.")

        query = str(query).strip()

        print("\n" + "=" * 60)
        print("TELECOM RAG QUERY")
        print("=" * 60)

        # STEP 1: RETRIEVAL

        print("\nRetrieving documents...")

        retrieved_documents = self.retriever.retrieve(
            query,
            top_k=retrieval_top_k
        )

        print(
            f"Retrieved documents: {len(retrieved_documents)}"
        )

        if not retrieved_documents:
            raise RuntimeError(
                "No relevant documents retrieved from Qdrant."
            )

        # STEP 2: RELEASE BGE AND QDRANT

        print("\nReleasing embedding and retrieval resources...")

        self.retriever.close()
        self.retriever = None

        gc.collect()

        # STEP 3: OPTIONAL RERANKING

        if self.use_reranker:

            print("\nLoading optional reranker...")

            self.reranker = Reranker()

            reranked_documents = self.reranker.rerank(
                query,
                retrieved_documents,
                top_k=rerank_top_k
            )

            reranked_count = len(reranked_documents)

        else:

            print("\nReranking disabled (low-memory mode).")

            reranked_documents = retrieved_documents[
                :rerank_top_k
            ]

            reranked_count = 0

        # STEP 4: CONTEXT BUILDING

        print("\nBuilding RAG context...")

        context_result = self.context_builder.build(
            query=query,
            documents=reranked_documents
        )

        context = context_result["context"]
        sources = context_result["sources"]

        print(f"Context length: {len(context)}")
        print(f"Sources included: {len(sources)}")

        # STEP 5: LOAD QWEN ONLY WHEN REQUIRED

        print("\nInitializing Qwen...")

        if self.llm is None:
            self.llm = QwenInference()

        # STEP 6: GENERATE ANSWER

        print("\nGenerating grounded answer with Qwen...")

        answer = self.llm.generate(
            prompt=self.prompt_manager.build(
                query=query,
                context=context
            ),
            max_new_tokens=max_new_tokens
        )

        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "retrieved_documents": retrieved_documents,
            "reranked_documents": reranked_documents,
            "context": context,
            "reranking_enabled": self.use_reranker,
            "reranked_count": reranked_count
        }

    def close(self):

        if self.retriever is not None:

            try:
                self.retriever.close()
            except Exception as error:
                print(f"Retriever cleanup warning: {error}")

            self.retriever = None

        if self.reranker is not None:

            try:
                del self.reranker
                self.reranker = None
            except Exception as error:
                print(f"Reranker cleanup warning: {error}")

        if self.llm is not None:

            try:
                self.llm.close()
            except Exception as error:
                print(f"Qwen cleanup warning: {error}")

            self.llm = None

        gc.collect()

        print("\nRAG Assistant resources released.")
