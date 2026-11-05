import json
import os


class IncidentMatcher:

    def __init__(self, rca_path="data/telelogs/rca_cases.json"):
        self.rca_path = rca_path
        self.rca_cases = self._load_rca_cases()

        self.anomaly_to_symptom = {
            "HIGH_LATENCY": "High Latency",
            "LOW_THROUGHPUT": "Low Throughput",
            "LOW_SINR": "Low SINR",
            "HIGH_PACKET_LOSS": "High Packet Loss",
            "CELL_OUTAGE": "No Signal",
        }

    def _load_rca_cases(self):

        if not os.path.exists(self.rca_path):
            return []

        with open(
            self.rca_path,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    def _normalize(self, text):

        if text is None:
            return ""

        return (
            str(text)
            .strip()
            .lower()
            .replace("_", " ")
        )

    def find_match(self, anomaly):

        anomaly_type = anomaly.get(
            "anomaly_type",
            ""
        )

        mapped_symptom = self.anomaly_to_symptom.get(
            anomaly_type
        )

        if not mapped_symptom:
            return None

        target = self._normalize(
            mapped_symptom
        )

        for case in self.rca_cases:

            symptoms = case.get(
                "symptoms",
                []
            )

            if not isinstance(symptoms, list):
                continue

            for symptom in symptoms:

                normalized = self._normalize(
                    symptom
                )

                if normalized == target:
                    return case

        return None

    def get_historical_root_cause(self, anomaly):

        match = self.find_match(anomaly)

        if match is None:
            return None

        return match.get("root_cause")

    def get_all_cases(self):
        return self.rca_cases

    def count_cases(self):
        return len(self.rca_cases)