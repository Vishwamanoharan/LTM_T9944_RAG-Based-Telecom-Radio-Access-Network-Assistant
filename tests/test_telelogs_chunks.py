from ingestion.embeddings.embedding_pipeline import (
    EmbeddingPipeline
)

pipeline = EmbeddingPipeline()

files = [
    "data/telelogs/incidents.json",
    "data/telelogs/rca_cases.json"
]

for file_path in files:

    chunks, embeddings = (
        pipeline.process_json(file_path)
    )

    print("\n================================")
    print(file_path)
    print("================================")

    print(
        f"Chunks: {len(chunks)}"
    )

    for i, chunk in enumerate(
        chunks[:10],
        start=1
    ):
        print(f"\nChunk {i}")
        print(chunk)