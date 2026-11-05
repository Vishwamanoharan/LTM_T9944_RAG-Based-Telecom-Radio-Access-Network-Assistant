import time

from ingestion.embeddings.embedding_pipeline import (
    EmbeddingPipeline
)


# =====================================================
# INITIALIZE PIPELINE
# =====================================================

print("\n====================================")
print("INITIALIZING INGESTION PIPELINE")
print("====================================")

pipeline = EmbeddingPipeline()


# =====================================================
# TEST TELEQNA
# =====================================================

print("\n\n====================================")
print("TESTING TELEQNA")
print("====================================")

start_time = time.time()

chunks, embeddings = pipeline.process_json(
    "data/teleqna/processed_teleqna.json"
)

elapsed = time.time() - start_time

print("\nTeleQnA completed")

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("Embedding dtype:", embeddings.dtype)
print("Processing time:", round(elapsed, 2), "seconds")

if chunks:
    print("\nFirst chunk:")
    print(chunks[0])


# =====================================================
# TEST ORANBENCH
# =====================================================

print("\n\n====================================")
print("TESTING ORANBENCH")
print("====================================")

start_time = time.time()

chunks, embeddings = pipeline.process_json(
    "data/oranbench/processed_oranbench.json"
)

elapsed = time.time() - start_time

print("\nORANBench completed")

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("Embedding dtype:", embeddings.dtype)
print("Processing time:", round(elapsed, 2), "seconds")

if chunks:
    print("\nFirst chunk:")
    print(chunks[0])


# =====================================================
# TEST 3GPP
# =====================================================

print("\n\n====================================")
print("TESTING 3GPP TS38.300")
print("====================================")

start_time = time.time()

chunks, embeddings = pipeline.process_pdf(
    "data/3gpp/TS38.300.pdf"
)

elapsed = time.time() - start_time

print("\n3GPP TS38.300 completed")

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("Embedding dtype:", embeddings.dtype)
print("Processing time:", round(elapsed, 2), "seconds")

if chunks:
    print("\nFirst chunk:")
    print(chunks[0])


# =====================================================
# FINAL RESULT
# =====================================================

print("\n\n====================================")
print("INGESTION PIPELINE TEST COMPLETED")
print("====================================")

print("\nAll datasets processed successfully.")

print("\nPipeline:")
print(
    "Parser → Chunker → BGE Embeddings"
)

print("\nNext step:")
print(
    "Store embeddings in FAISS / Qdrant"
)

print("====================================\n")