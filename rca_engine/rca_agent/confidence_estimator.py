# rca_engine/rca_agent/confidence_estimator.py


class ConfidenceEstimator:

    def estimate(
        self,
        anomaly
    ):

        severity = anomaly[
            "severity"
        ]

        event = anomaly.get(
            "event",
            "NORMAL"
        )

        score = 0.60

        if severity == "WARNING":

            score += 0.10

        elif severity == "CRITICAL":

            score += 0.25

        if event != "NORMAL":

            score += 0.10

        return round(
            min(score, 0.99),
            2
        )

    # Backward compatibility
    def estimate_confidence(
        self,
        anomaly
    ):
        return self.estimate(
            anomaly
        )