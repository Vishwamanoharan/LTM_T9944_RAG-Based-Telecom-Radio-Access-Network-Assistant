# anomaly_detection/anomaly_engine/alert_generator.py


class AlertGenerator:

    def generate_alert(
        self,
        tower_id,
        anomaly_type,
        severity,
        metric,
        value,
        event
    ):

        return {

            "tower_id":
                tower_id,

            "anomaly_type":
                anomaly_type,

            "severity":
                severity,

            "metric":
                metric,

            "value":
                value,

            "event":
                event
        }


if __name__ == "__main__":

    generator = AlertGenerator()

    alert = generator.generate_alert(

        tower_id="Tower-001",

        anomaly_type="HIGH_LATENCY",

        severity="CRITICAL",

        metric="latency_ms",

        value=180,

        event="BACKHAUL_FAILURE"
    )

    print(alert)