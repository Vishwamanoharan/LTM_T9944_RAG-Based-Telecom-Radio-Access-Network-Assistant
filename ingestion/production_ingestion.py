
import json
import hashlib
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from ingestion.embeddings.embedding_generator import EmbeddingGenerator


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

QDRANT_PATH = str(ROOT / "vector_db" / "qdrant_data")
COLLECTION_NAME = "telecom_rag"

VECTOR_SIZE = 384
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
INSERT_BATCH_SIZE = 64


# --------------------------------------------------
# TEXT CHUNKING
# --------------------------------------------------

def split_text(text):
    text = str(text).strip()

    if not text:
        return []

    chunks = []
    start = 0
    step = CHUNK_SIZE - CHUNK_OVERLAP

    while start < len(text):
        chunk = text[start:start + CHUNK_SIZE].strip()

        if chunk:
            chunks.append(chunk)

        start += step

    return chunks


# --------------------------------------------------
# JSON LOADER
# --------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# DATASET FORMATTERS
# --------------------------------------------------

def format_teleqna(record):
    choices = record.get("choices", [])
    answer = record.get("answer", "")

    if isinstance(answer, int) and isinstance(choices, list):
        if 0 <= answer < len(choices):
            answer_text = choices[answer]
        else:
            answer_text = str(answer)
    else:
        answer_text = str(answer)

    return "\n".join([
        f"Question: {record.get('question', '')}",
        f"Choices: {' | '.join(map(str, choices))}",
        f"Correct answer: {answer_text}",
        f"Explanation: {record.get('explaination', record.get('explanation', ''))}"
    ])


def format_oranbench(record):
    return "\n".join([
        f"Question: {record.get('question', '')}",
        f"Answer: {record.get('answer', '')}",
        f"Difficulty: {record.get('difficulty', '')}"
    ])


def format_telelogs(record):
    return "\n".join([
        f"Question: {record.get('question', '')}",
        f"Answer: {record.get('answer', '')}"
    ])


def format_rca_case(record):
    symptoms = record.get("symptoms", [])

    return "\n".join([
        f"Symptoms: {'; '.join(map(str, symptoms))}",
        f"Root cause: {record.get('root_cause', '')}"
    ])


# --------------------------------------------------
# QDRANT COLLECTION
# --------------------------------------------------

def initialize_collection(client):

    collections = client.get_collections().collections

    exists = any(
        item.name == COLLECTION_NAME
        for item in collections
    )

    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )

        print("Production collection created.")

    else:
        info = client.get_collection(COLLECTION_NAME)

        actual_size = info.config.params.vectors.size

        if actual_size != VECTOR_SIZE:
            raise ValueError(
                f"Collection dimension mismatch: {actual_size}"
            )

        print("Existing production collection detected.")


# --------------------------------------------------
# INGESTION ENGINE
# --------------------------------------------------

class ProductionIngestion:

    def __init__(self):

        print("\nInitializing production ingestion...")

        self.client = QdrantClient(path=QDRANT_PATH)

        initialize_collection(self.client)

        self.embedder = EmbeddingGenerator()

        self.buffer = []
        self.total_inserted = 0

    def add_record(
        self,
        text,
        dataset,
        source,
        document,
        record_id,
        extra_metadata=None
    ):

        chunks = split_text(text)

        for index, chunk in enumerate(chunks):

            metadata = {
                "dataset": dataset,
                "source": source,
                "document": document,
                "record_id": str(record_id),
                "chunk_index": index
            }

            if extra_metadata:
                metadata.update(extra_metadata)

            self.buffer.append((chunk, metadata))

            if len(self.buffer) >= INSERT_BATCH_SIZE:
                self.flush()

    def flush(self):

        if not self.buffer:
            return

        texts = [
            item[0]
            for item in self.buffer
        ]

        vectors = self.embedder.generate(texts)

        if vectors.shape != (len(texts), VECTOR_SIZE):
            raise ValueError(
                f"Unexpected embedding shape: {vectors.shape}"
            )

        points = []

        for (chunk, metadata), vector in zip(
            self.buffer,
            vectors
        ):

            identity = (
                f"{metadata['dataset']}|"
                f"{metadata['document']}|"
                f"{metadata['record_id']}|"
                f"{metadata['chunk_index']}"
            )

            point_id = str(
                uuid5(NAMESPACE_URL, identity)
            )

            payload = dict(metadata)
            payload["text"] = chunk

            points.append(
                PointStruct(
                    id=point_id,
                    vector=np.asarray(
                        vector,
                        dtype=np.float32
                    ).tolist(),
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True
        )

        self.total_inserted += len(points)

        print(
            f"Inserted/upserted: {self.total_inserted} vectors"
        )

        self.buffer.clear()

    # --------------------------------------------------
    # TELEQNA
    # --------------------------------------------------

    def ingest_teleqna(self):

        path = ROOT / "data/teleqna/processed_teleqna.json"
        records = load_json(path)

        print(f"\nIngesting TeleQnA: {len(records)} records")

        for index, record in enumerate(records):

            text = format_teleqna(record)

            self.add_record(
                text=text,
                dataset="TeleQnA",
                source="TeleQnA",
                document="processed_teleqna.json",
                record_id=index,
                extra_metadata={
                    "subject": str(record.get("subject", ""))
                }
            )

        self.flush()

    # --------------------------------------------------
    # ORANBENCH
    # --------------------------------------------------

    def ingest_oranbench(self):

        path = ROOT / "data/oranbench/processed_oranbench.json"
        records = load_json(path)

        print(f"\nIngesting ORANBench: {len(records)} records")

        for index, record in enumerate(records):

            text = format_oranbench(record)

            self.add_record(
                text=text,
                dataset="ORANBench",
                source="ORANBench",
                document="processed_oranbench.json",
                record_id=index,
                extra_metadata={
                    "difficulty": str(
                        record.get("difficulty", "")
                    )
                }
            )

        self.flush()

    # --------------------------------------------------
    # 3GPP
    # --------------------------------------------------

    def ingest_3gpp(self):

        path = ROOT / "data/3gpp/processed_specs.json"
        records = load_json(path)

        print(f"\nIngesting 3GPP: {len(records)} documents")

        for index, record in enumerate(records):

            text = record.get("text", "")

            document = record.get(
                "document",
                f"3GPP_document_{index}"
            )

            self.add_record(
                text=text,
                dataset="3GPP",
                source="3GPP",
                document=document,
                record_id=document
            )

        self.flush()

    # --------------------------------------------------
    # TELELOGS Q&A
    # --------------------------------------------------

    def ingest_telelogs(self):

        path = ROOT / "data/telelogs/telelogs.json"
        records = load_json(path)

        print(f"\nIngesting TeleLogs Q&A: {len(records)} records")

        for index, record in enumerate(records):

            text = format_telelogs(record)

            self.add_record(
                text=text,
                dataset="TeleLogs",
                source="TeleLogs",
                document="telelogs.json",
                record_id=index
            )

        self.flush()

    # --------------------------------------------------
    # TELELOGS INCIDENTS
    # --------------------------------------------------

    def ingest_incidents(self):

        path = ROOT / "data/telelogs/incidents.json"
        records = load_json(path)

        print(f"\nIngesting incidents: {len(records)} records")

        incident_groups = {}

        for record in records:

            incident = str(
                record.get("incident", "Unknown")
            )

            incident_groups.setdefault(
                incident,
                []
            ).append(record)

        for incident, group in incident_groups.items():

            towers = sorted(set(
                str(record.get("tower", ""))
                for record in group
            ))

            text = (
                f"Incident type: {incident}\n"
                f"Total incident records: {len(group)}\n"
                f"Affected towers: {', '.join(towers)}"
            )

            self.add_record(
                text=text,
                dataset="TeleLogs",
                source="TeleLogs",
                document="incidents.json",
                record_id=f"incident_{incident}"
            )

        self.flush()

    # --------------------------------------------------
    # TELELOGS RCA CASES
    # --------------------------------------------------

    def ingest_rca_cases(self):

        path = ROOT / "data/telelogs/rca_cases.json"
        records = load_json(path)

        print(f"\nIngesting TeleLogs RCA: {len(records)} cases")

        for index, record in enumerate(records):

            text = format_rca_case(record)

            self.add_record(
                text=text,
                dataset="TeleLogs",
                source="TeleLogs",
                document="rca_cases.json",
                record_id=index
            )

        self.flush()

    # --------------------------------------------------
    # RUN ALL
    # --------------------------------------------------

    def run(self):

        try:

            self.ingest_teleqna()
            self.ingest_oranbench()
            self.ingest_3gpp()
            self.ingest_telelogs()
            self.ingest_incidents()
            self.ingest_rca_cases()

            self.flush()

            info = self.client.get_collection(
                COLLECTION_NAME
            )

            print("\n" + "=" * 60)
            print("PRODUCTION INGESTION COMPLETED")
            print("=" * 60)

            print(
                "Vectors inserted/upserted:",
                self.total_inserted
            )

            print(
                "Total collection vectors:",
                info.points_count
            )

            print(
                "Vector dimensions:",
                info.config.params.vectors.size
            )

        finally:
            self.client.close()


if __name__ == "__main__":

    ingestion = ProductionIngestion()
    ingestion.run()
