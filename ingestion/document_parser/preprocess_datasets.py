
import json
import pandas as pd
from pathlib import Path
from pypdf import PdfReader


# =====================================================
# PATHS
# =====================================================

DATA_DIR = Path("data")

TELEQNA_DIR = DATA_DIR / "teleqna"
ORAN_DIR = DATA_DIR / "oranbench"
GPP_DIR = DATA_DIR / "3gpp"
TELELOGS_DIR = DATA_DIR / "telelogs"


# =====================================================
# TELEQNA PROCESSING
# =====================================================

print("Processing TeleQnA...")

with open(
    TELEQNA_DIR / "teleqna.json",
    "r",
    encoding="utf-8"
) as f:
    teleqna = json.load(f)

processed = []

for row in teleqna:

    processed.append({
        "source": "TeleQnA",
        "question": row.get("question", ""),
        "choices": row.get("choices", []),
        "answer": row.get("answer", ""),
        "subject": row.get("subject", ""),
        "explaination": row.get("explaination", "")
    })

with open(
    TELEQNA_DIR / "processed_teleqna.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        processed,
        f,
        indent=2,
        ensure_ascii=False
    )

print("processed_teleqna.json created")


# =====================================================
# ORANBENCH PROCESSING
# =====================================================

print("Processing ORANBench...")

with open(
    ORAN_DIR / "oranbench.json",
    "r",
    encoding="utf-8"
) as f:
    oran = json.load(f)

processed = []

for row in oran:

    processed.append({
        "source": "ORANBench",
        "question": row.get("question", ""),
        "answer": row.get("answer", ""),
        "difficulty": row.get("difficulty", "")
    })

with open(
    ORAN_DIR / "processed_oranbench.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        processed,
        f,
        indent=2,
        ensure_ascii=False
    )

print("processed_oranbench.json created")


# =====================================================
# CHUNK FUNCTION
# =====================================================

def create_chunks(records, source_name):

    chunks = []

    chunk_id = 1

    for row in records:

        question = row.get(
            "question",
            ""
        )

        answer = row.get(
            "answer",
            ""
        )

        subject = row.get(
            "subject",
            ""
        )

        difficulty = row.get(
            "difficulty",
            ""
        )

        choices = row.get(
            "choices",
            []
        )

        explanation = row.get(
            "explaination",
            ""
        )

        # -------------------------------------------------
        # Format choices clearly
        # -------------------------------------------------

        if isinstance(choices, list):

            formatted_choices = "\n".join(
                f"{index}: {choice}"
                for index, choice in enumerate(choices)
            )

        elif isinstance(choices, dict):

            formatted_choices = "\n".join(
                f"{key}: {value}"
                for key, value in choices.items()
            )

        else:

            formatted_choices = str(
                choices
            )

        # -------------------------------------------------
        # Build source-specific chunk
        # -------------------------------------------------

        if source_name == "TeleQnA":

            text = (
                f"Source: TeleQnA\n"
                f"Question: {question}\n"
                f"Choices:\n"
                f"{formatted_choices}\n"
                f"Correct Answer: {answer}\n"
                f"Subject: {subject}\n"
                f"Explanation: {explanation}"
            )

        elif source_name == "ORANBench":

            text = (
                f"Source: ORANBench\n"
                f"Question: {question}\n"
                f"Choices:\n"
                f"{formatted_choices}\n"
                f"Correct Answer: {answer}\n"
                f"Difficulty: {difficulty}"
            )

        else:

            text = (
                f"Source: {source_name}\n"
                f"Question: {question}\n"
                f"Answer: {answer}"
            )

        chunks.append({
            "chunk_id": chunk_id,
            "source": source_name,
            "text": text
        })

        chunk_id += 1

    return chunks


# =====================================================
# TELEQNA CHUNKS
# =====================================================

with open(
    TELEQNA_DIR / "processed_teleqna.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

chunks = create_chunks(
    data,
    "TeleQnA"
)

with open(
    TELEQNA_DIR / "chunks.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print("TeleQnA chunks.json created")


# =====================================================
# ORANBENCH CHUNKS
# =====================================================

with open(
    ORAN_DIR / "processed_oranbench.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

chunks = create_chunks(
    data,
    "ORANBench"
)

with open(
    ORAN_DIR / "chunks.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print("ORANBench chunks.json created")


# =====================================================
# 3GPP PDF EXTRACTION
# =====================================================

print("Processing 3GPP PDFs...")

specs = []

pdf_files = [
    "TS38.300.pdf",
    "TS38.331.pdf",
    "TS38.401.pdf"
]

for pdf_name in pdf_files:

    pdf_path = GPP_DIR / pdf_name

    if not pdf_path.exists():
        continue

    reader = PdfReader(
        str(pdf_path)
    )

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    specs.append({
        "source": "3GPP",
        "document": pdf_name,
        "text": text[:50000]
    })

with open(
    GPP_DIR / "processed_specs.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        specs,
        f,
        indent=2,
        ensure_ascii=False
    )

print("processed_specs.json created")


# =====================================================
# TELELOGS PROCESSING
# =====================================================

print("Processing TeleLogs...")

with open(
    TELELOGS_DIR / "telelogs.json",
    "r",
    encoding="utf-8"
) as f:
    telelogs = json.load(f)


# ---------------------------------------------
# telelogs.csv
# ---------------------------------------------

rows = []

for i, row in enumerate(telelogs):

    rows.append({
        "timestamp": f"2026-01-{(i % 28) + 1}",
        "tower_id": f"T{(i % 20) + 1}",
        "alarm": row.get("question", ""),
        "kpi": "Latency",
        "severity": "Medium"
    })

df = pd.DataFrame(
    rows
)

df.to_csv(
    TELELOGS_DIR / "telelogs.csv",
    index=False
)

print("telelogs.csv created")


# ---------------------------------------------
# incidents.json
# ---------------------------------------------

incidents = []

for i in range(50):

    incidents.append({
        "incident_id": i + 1,
        "tower": f"T{(i % 20) + 1}",
        "incident": "Interference"
    })

with open(
    TELELOGS_DIR / "incidents.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        incidents,
        f,
        indent=2
    )

print("incidents.json created")


# ---------------------------------------------
# rca_cases.json
# ---------------------------------------------

rca_cases = [
    {
        "symptoms": [
            "Low SINR",
            "High Packet Loss"
        ],
        "root_cause": "Interference"
    },
    {
        "symptoms": [
            "High Latency",
            "Low Throughput"
        ],
        "root_cause": "Congestion"
    },
    {
        "symptoms": [
            "No Signal"
        ],
        "root_cause": "Tower Outage"
    }
]

with open(
    TELELOGS_DIR / "rca_cases.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        rca_cases,
        f,
        indent=2
    )

print("rca_cases.json created")


print("\n===================================")
print("PHASE 1 COMPLETED SUCCESSFULLY")
print("===================================")
