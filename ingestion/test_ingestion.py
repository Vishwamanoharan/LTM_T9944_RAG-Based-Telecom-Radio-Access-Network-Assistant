from ingestion.embeddings.embedding_pipeline import (
    EmbeddingPipeline
)


pipeline = EmbeddingPipeline()


# =====================================================
# TEST TELEQNA
# =====================================================

print("\nTesting TeleQnA...")

chunks, embeddings = pipeline.process_json(
    "data/teleqna/processed_teleqna.json"
)

print("Number of chunks:", len(chunks))

print(
    "Embedding shape:",
    embeddings.shape
)

print("\nFirst chunk:")

print(chunks[0])


# =====================================================
# TEST ORANBENCH
# =====================================================

print("\nTesting ORANBench...")

chunks, embeddings = pipeline.process_json(
    "data/oranbench/processed_oranbench.json"
)

print("Number of chunks:", len(chunks))

print(
    "Embedding shape:",
    embeddings.shape
)


# =====================================================
# TEST 3GPP
# =====================================================

print("\nTesting 3GPP...")

chunks, embeddings = pipeline.process_pdf(
    "data/3gpp/TS38.300.pdf"
)

print("Number of chunks:", len(chunks))

print(
    "Embedding shape:",
    embeddings.shape
)


print("\n====================================")
print("INGESTION PIPELINE TEST COMPLETED")
print("====================================")