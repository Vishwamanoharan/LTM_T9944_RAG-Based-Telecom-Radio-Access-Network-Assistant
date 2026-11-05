from datasets import load_dataset
import json
from pathlib import Path


# ============================================================
# Create required data directories
# ============================================================

Path("data/teleqna").mkdir(parents=True, exist_ok=True)
Path("data/oranbench").mkdir(parents=True, exist_ok=True)
Path("data/telelogs").mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. DOWNLOAD TELEQNA
# ============================================================

print("\nDownloading TeleQnA...")

dataset = load_dataset("netop/TeleQnA")

print("TeleQnA splits:")
print(dataset)

records = dataset["test"].to_list()

output_file = "data/teleqna/teleqna.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        records,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"TeleQnA saved to: {output_file}")
print(f"Records: {len(records)}")

# ============================================================
# 2. DOWNLOAD ORANBENCH
# ============================================================

print("\nDownloading ORANBench...")

dataset = load_dataset("prnshv/ORANBench")

print("ORANBench splits:")
print(dataset)

# Use train split
train_data = dataset["train"]

records = train_data.to_list()

output_file = "data/oranbench/oranbench.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        records,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"ORANBench saved to: {output_file}")
print(f"Records: {len(records)}")


# ============================================================
# 3. DOWNLOAD TELELOGS
# ============================================================

print("\nDownloading TeleLogs...")

dataset = load_dataset("netop/TeleLogs")

print("TeleLogs splits:")
print(dataset)

# Use test split
test_data = dataset["test"]

records = test_data.to_list()

# Save as JSON temporarily
output_file = "data/telelogs/telelogs.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        records,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"TeleLogs saved to: {output_file}")
print(f"Records: {len(records)}")


# ============================================================
# COMPLETE
# ============================================================

print("\n==========================================")
print("All datasets downloaded successfully!")
print("==========================================")