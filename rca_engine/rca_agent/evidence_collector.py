# rca_engine/rca_agent/evidence_collector.py


class EvidenceCollector:

    def collect(
        self,
        anomaly
    ):

        evidence = []

        anomaly_type = anomaly[
            "anomaly_type"
        ]

        metric = anomaly[
            "metric"
        ]

        value = anomaly[
            "value"
        ]

        threshold = anomaly[
            "threshold"
        ]

        event = anomaly[
            "event"
        ]

        evidence.append(
            f"{metric}={value}"
        )

        evidence.append(
            f"threshold={threshold}"
        )

        if event != "NORMAL":

            evidence.append(
                f"event={event}"
            )

        # -------------------------------------------------
        # Anomaly specific evidence
        # -------------------------------------------------

        if anomaly_type == "HIGH_LATENCY":

            evidence.append(
                "Network delay increased"
            )

        elif anomaly_type == "HIGH_PACKET_LOSS":

            evidence.append(
                "Packet delivery degradation detected"
            )

        elif anomaly_type == "LOW_SINR":

            evidence.append(
                "Radio signal quality degraded"
            )

        elif anomaly_type == "LOW_THROUGHPUT":

            evidence.append(
                "User throughput reduced"
            )

        elif anomaly_type == "HIGH_PRB_UTILIZATION":

            evidence.append(
                "Radio resources heavily utilized"
            )

        elif anomaly_type == "HIGH_CPU_UTILIZATION":

            evidence.append(
                "Base station processing load high"
            )

        elif anomaly_type == "CELL_OUTAGE":

            evidence.append(
                "Cell unavailable"
            )

        elif anomaly_type == "POWER_FAILURE":

            evidence.append(
                "Power infrastructure failure"
            )

        return evidence