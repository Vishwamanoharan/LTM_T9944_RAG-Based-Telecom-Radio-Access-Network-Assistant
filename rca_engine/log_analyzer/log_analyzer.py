import os
import pandas as pd


class LogAnalyzer:

    def __init__(self, log_path="data/telelogs/telelogs.csv"):
        self.log_path = log_path
        self.logs = self._load_logs()

    def _load_logs(self):
        if not os.path.exists(self.log_path):
            return pd.DataFrame()

        return pd.read_csv(self.log_path)

    def get_statistics(self):
        if self.logs.empty:
            return {
            "total_records": 0,
            "columns": []
        }
        return {
        "total_records": len(self.logs),
        "columns": list(self.logs.columns)
    }

    # Backward-compatible method used by the existing tests.
    def get_log_statistics(self):
        return self.get_statistics()

    def search_keyword(self, keyword):
        if self.logs.empty or not keyword:
            return pd.DataFrame()

        keyword = str(keyword).lower()

        mask = self.logs.astype(str).apply(
            lambda column: column.str.lower().str.contains(
                keyword,
                na=False,
                regex=False
            )
        ).any(axis=1)

        return self.logs[mask]

    def find_related_logs(self, anomaly, limit=20):
        if self.logs.empty:
            return pd.DataFrame()

        anomaly_type = str(
            anomaly.get("anomaly_type", "")
        ).lower()

        event = str(
            anomaly.get("event", "")
        ).lower()

        metric = str(
            anomaly.get("metric", "")
        ).lower()

        keywords = []

        if anomaly_type:
            keywords.append(anomaly_type)

        if event and event != "normal":
            keywords.append(event)

        if metric:
            keywords.append(metric)

        keyword_map = {
            "high_latency": [
                "latency",
                "delay"
            ],
            "high_packet_loss": [
                "packet loss",
                "packet_loss"
            ],
            "low_sinr": [
                "sinr",
                "interference"
            ],
            "low_throughput": [
                "throughput"
            ],
            "high_prb_utilization": [
                "prb",
                "utilization"
            ],
            "high_cpu_utilization": [
                "cpu"
            ],
            "cell_outage": [
                "outage",
                "cell"
            ],
            "power_failure": [
                "power"
            ],
            "backhaul_failure": [
                "backhaul"
            ],
            "congestion": [
                "congestion"
            ],
            "interference": [
                "interference"
            ]
        }

        expanded_keywords = []

        for keyword in keywords:
            expanded_keywords.append(keyword)

            if keyword in keyword_map:
                expanded_keywords.extend(
                    keyword_map[keyword]
                )

        expanded_keywords = list(
            dict.fromkeys(expanded_keywords)
        )

        matched_rows = []

        for keyword in expanded_keywords:

            if not keyword:
                continue

            matches = self.search_keyword(keyword)

            if not matches.empty:
                matched_rows.append(matches)

        if not matched_rows:
            return pd.DataFrame()

        result = pd.concat(
            matched_rows,
            ignore_index=True
        ).drop_duplicates()

        return result.head(limit)

    def count_related_logs(self, anomaly):
        return len(
            self.find_related_logs(anomaly)
        )