# tests/test_rca.py

from rca_engine.rca_agent.evidence_collector import (
    EvidenceCollector
)

from rca_engine.rca_agent.root_cause_engine import (
    RootCauseEngine
)

from rca_engine.rca_agent.confidence_estimator import (
    ConfidenceEstimator
)

from rca_engine.recommendation_engine.recommendation_generator import (
    RecommendationGenerator
)


def test_rca():

    print()
    print("=" * 40)
    print("RCA ENGINE TEST")
    print("=" * 40)

    anomaly = {

        "tower_id":
            "Tower-001",

        "anomaly_type":
            "HIGH_LATENCY",

        "severity":
            "CRITICAL",

        "metric":
            "latency_ms",

        "value":
            180,

        "threshold":
            100,

        "event":
            "BACKHAUL_FAILURE"
    }

    collector = EvidenceCollector()

    rca_engine = RootCauseEngine()

    estimator = ConfidenceEstimator()

    recommender = (
        RecommendationGenerator()
    )

    evidence = collector.collect(
        anomaly
    )

    root_cause = (
        rca_engine.determine_root_cause(
            anomaly
        )
    )

    confidence = (
        estimator.estimate(
            anomaly
        )
    )

    recommendation = (
        recommender.generate(
            root_cause
        )
    )

    print()
    print(
        f"Tower ID: {anomaly['tower_id']}"
    )

    print(
        f"Anomaly: {anomaly['anomaly_type']}"
    )

    print(
        f"Root Cause: {root_cause}"
    )

    print(
        f"Confidence: {confidence}"
    )

    print(
        f"Recommendation: {recommendation}"
    )

    print()
    print("Evidence:")

    for item in evidence:

        print(f" - {item}")

    assert root_cause == (
        "BACKHAUL_FAILURE"
    )

    assert confidence > 0.8

    assert len(evidence) > 0

    print()
    print("=" * 40)
    print("RCA TEST PASSED")
    print("=" * 40)


if __name__ == "__main__":

    test_rca()