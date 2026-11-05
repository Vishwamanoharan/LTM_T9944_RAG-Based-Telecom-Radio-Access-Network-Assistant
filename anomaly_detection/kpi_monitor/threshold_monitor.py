# anomaly_detection/kpi_monitor/threshold_monitor.py

class ThresholdMonitor:

    def __init__(self):

        self.thresholds = {

            "latency_ms": 50,

            "packet_loss_pct": 2,

            "sinr_db": 10,

            "prb_utilization_pct": 85,

            "cpu_utilization_pct": 80,

            "throughput_mbps": 100
        }

    def get_thresholds(self):

        return self.thresholds

    def check_metric(
        self,
        metric_name,
        value
    ):

        if metric_name not in self.thresholds:
            return False

        threshold = self.thresholds[metric_name]

        if metric_name == "throughput_mbps":

            return value < threshold

        return value > threshold


if __name__ == "__main__":

    monitor = ThresholdMonitor()

    print(monitor.get_thresholds())