# tests/reset_collection.py

from qdrant_client import QdrantClient


client = QdrantClient(
    path="vector_db/qdrant_data"
)

collection_name = "telecom_rag"

try:

    client.delete_collection(
        collection_name
    )

    print(
        f"Deleted: {collection_name}"
    )

except Exception as e:

    print(e)

finally:

    client.close()