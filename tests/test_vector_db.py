
from vector_db.qdrant.qdrant_client import (
    QdrantDBClient
)

from vector_db.qdrant.collection_manager import (
    CollectionManager
)

from vector_db.qdrant.vector_store import (
    VectorStore
)


# =====================================================
# CONFIGURATION
# =====================================================

COLLECTION_NAME = "telecom_rag_test"

VECTOR_SIZE = 384

QDRANT_PATH = "vector_db/qdrant_test_data"


# =====================================================
# TEST QDRANT CONNECTION
# =====================================================

def test_qdrant_connection():

    print("\n========================================")
    print("TEST 1: QDRANT CONNECTION")
    print("========================================")

    db = QdrantDBClient(
        path=QDRANT_PATH
    )

    client = db.get_client()

    assert client is not None

    print("Qdrant client created successfully.")

    db.close()


# =====================================================
# TEST COLLECTION CREATION
# =====================================================

def test_collection_creation():

    print("\n========================================")
    print("TEST 2: COLLECTION CREATION")
    print("========================================")

    db = QdrantDBClient(
        path=QDRANT_PATH
    )

    client = db.get_client()

    collection_manager = CollectionManager(
        client,
        collection_name=COLLECTION_NAME
    )

    collection_manager.create_collection(
        vector_size=VECTOR_SIZE
    )

    assert collection_manager.collection_exists()

    print(
        f"Collection '{COLLECTION_NAME}' "
        "created successfully."
    )

    db.close()


# =====================================================
# TEST VECTOR INSERTION
# =====================================================

def test_vector_insertion():

    print("\n========================================")
    print("TEST 3: VECTOR INSERTION")
    print("========================================")

    db = QdrantDBClient(
        path=QDRANT_PATH
    )

    client = db.get_client()

    collection_manager = CollectionManager(
        client,
        collection_name=COLLECTION_NAME
    )

    collection_manager.create_collection(
        vector_size=VECTOR_SIZE
    )

    vector_store = VectorStore(
        client,
        collection_name=COLLECTION_NAME
    )

    # -------------------------------------------------
    # TEST DATA
    # -------------------------------------------------

    chunks = [
        "5G NR uses NG-RAN for radio access.",
        "High latency can be caused by network congestion.",
        "SINR degradation may indicate radio interference."
    ]

    embeddings = [
        [0.01] * VECTOR_SIZE,
        [0.02] * VECTOR_SIZE,
        [0.03] * VECTOR_SIZE
    ]

    metadata = [
        {
            "dataset": "TeleQnA",
            "source": "TeleQnA"
        },
        {
            "dataset": "TeleLogs",
            "source": "TeleLogs",
            "document": "incidents.json"
        },
        {
            "dataset": "3GPP",
            "source": "3GPP",
            "document": "TS38.300.pdf",
            "page": 10
        }
    ]

    vector_store.insert(
        chunks,
        embeddings,
        metadata=metadata
    )

    count = vector_store.count()

    print(
        f"Vectors stored: {count}"
    )

    assert count >= 3

    print(
        "Vector insertion successful."
    )

    db.close()


# =====================================================
# TEST VECTOR SEARCH
# =====================================================

def test_vector_search():

    print("\n========================================")
    print("TEST 4: VECTOR SEARCH")
    print("========================================")

    db = QdrantDBClient(
        path=QDRANT_PATH
    )

    client = db.get_client()

    vector_store = VectorStore(
        client,
        collection_name=COLLECTION_NAME
    )

    query_vector = [
        0.01
    ] * VECTOR_SIZE

    results = vector_store.search(
        query_vector,
        limit=3
    )

    print(
        f"Search results: {len(results)}"
    )

    assert len(results) > 0

    print("\nTop result:")

    top_result = results[0]

    print(
        "Score:",
        top_result.score
    )

    print(
        "Payload:",
        top_result.payload
    )

    db.close()


# =====================================================
# TEST METADATA
# =====================================================

def test_metadata():

    print("\n========================================")
    print("TEST 5: METADATA")
    print("========================================")

    db = QdrantDBClient(
        path=QDRANT_PATH
    )

    client = db.get_client()

    vector_store = VectorStore(
        client,
        collection_name=COLLECTION_NAME
    )

    query_vector = [
        0.01
    ] * VECTOR_SIZE

    results = vector_store.search(
        query_vector,
        limit=3
    )

    assert len(results) > 0

    for result in results:

        payload = result.payload

        print("\nPayload:")
        print(payload)

        assert "text" in payload

    db.close()


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("\n")
    print("========================================")
    print("QDRANT VECTOR DB TEST")
    print("========================================")

    test_qdrant_connection()

    test_collection_creation()

    test_vector_insertion()

    test_vector_search()

    test_metadata()

    print("\n========================================")
    print("ALL VECTOR DB TESTS PASSED")
    print("========================================")

