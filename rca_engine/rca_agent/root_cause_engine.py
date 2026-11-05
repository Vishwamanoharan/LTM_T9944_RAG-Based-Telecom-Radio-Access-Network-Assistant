# rca_engine/rca_agent/root_cause_engine.py


class RootCauseEngine:

    ROOT_CAUSES = {

        "HIGH_LATENCY":
            "NETWORK_CONGESTION",

        "HIGH_PACKET_LOSS":
            "NETWORK_DEGRADATION",

        "LOW_SINR":
            "RADIO_INTERFERENCE",

        "LOW_THROUGHPUT":
            "RADIO_DEGRADATION",

        "HIGH_PRB_UTILIZATION":
            "RESOURCE_CONGESTION",

        "HIGH_CPU_UTILIZATION":
            "PROCESSING_OVERLOAD",

        "CELL_OUTAGE":
            "CELL_FAILURE",

        "POWER_FAILURE":
            "POWER_ISSUE"
    }

    EVENT_OVERRIDES = {

        "CONGESTION":
            "NETWORK_CONGESTION",

        "INTERFERENCE":
            "RADIO_INTERFERENCE",

        "BACKHAUL_FAILURE":
            "BACKHAUL_FAILURE",

        "CELL_OUTAGE":
            "CELL_FAILURE",

        "POWER_FAILURE":
            "POWER_ISSUE",

        "HIGH_CPU_LOAD":
            "PROCESSING_OVERLOAD"
    }

    def determine_root_cause(
        self,
        anomaly
    ):

        event = anomaly.get(
            "event",
            "NORMAL"
        )

        if event in self.EVENT_OVERRIDES:

            return self.EVENT_OVERRIDES[
                event
            ]

        anomaly_type = anomaly[
            "anomaly_type"
        ]

        return self.ROOT_CAUSES.get(
            anomaly_type,
            "UNKNOWN"
        )