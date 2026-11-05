from qdrant_client import QdrantClient

client = QdrantClient(
    path="vector_db/qdrant_data"
)

try:

    info = client.get_collection(
        collection_name="telecom_rag"
    )

    print("\nCollection Info:\n")
    print(info)

except Exception as e:

    print(
        "\nCollection does not exist."
    )

    print(e)

finally:

    try:
        client.close()
    except:
        pass