# anomaly_detection/anomaly_engine/severity_classifier.py


class SeverityClassifier:

    def classify(
        self,
        metric,
        value
    ):

        if metric == "latency_ms":

            if value > 150:
                return "CRITICAL"

            if value > 80:
                return "WARNING"

        elif metric == "packet_loss_pct":

            if value > 5:
                return "CRITICAL"

            if value > 2:
                return "WARNING"

        elif metric == "sinr_db":

            if value < 5:
                return "CRITICAL"

            if value < 10:
                return "WARNING"

        elif metric == "prb_utilization_pct":

            if value > 95:
                return "CRITICAL"

            if value > 85:
                return "WARNING"

        elif metric == "cpu_utilization_pct":

            if value > 95:
                return "CRITICAL"

            if value > 80:
                return "WARNING"

        elif metric == "throughput_mbps":

            if value < 50:
                return "CRITICAL"

            if value < 100:
                return "WARNING"

        return "INFO"


if __name__ == "__main__":

    classifier = SeverityClassifier()

    print(
        classifier.classify(
            "latency_ms",
            170
        )
    )