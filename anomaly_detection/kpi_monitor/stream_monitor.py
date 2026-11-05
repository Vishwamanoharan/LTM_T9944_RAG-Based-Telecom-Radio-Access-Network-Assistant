# anomaly_detection/kpi_monitor/stream_monitor.py

from anomaly_detection.kpi_monitor.threshold_monitor import (
    ThresholdMonitor
)


class StreamMonitor:

    def __init__(self):

        self.threshold_monitor = (
            ThresholdMonitor()
        )

    def monitor_tower(
        self,
        kpi_record
    ):

        alerts = []

        thresholds = (
            self.threshold_monitor
            .get_thresholds()
        )

        for metric, threshold in thresholds.items():

            if metric not in kpi_record:
                continue

            value = kpi_record[metric]

            if metric == "throughput_mbps":

                if value < threshold:

                    alerts.append(
                        {
                            "tower_id":
                                kpi_record["tower_id"],
                            "metric":
                                metric,
                            "value":
                                value,
                            "threshold":
                                threshold
                        }
                    )

            else:

                if value > threshold:

                    alerts.append(
                        {
                            "tower_id":
                                kpi_record["tower_id"],
                            "metric":
                                metric,
                            "value":
                                value,
                            "threshold":
                                threshold
                        }
                    )

        return alerts


if __name__ == "__main__":

    sample = {

        "tower_id": "Tower-001",

        "latency_ms": 120,

        "packet_loss_pct": 5
    }

    monitor = StreamMonitor()

    print(
        monitor.monitor_tower(sample)
    )