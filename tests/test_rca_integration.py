# tests/test_rca_integration.py

from rca_engine.rca_agent.rca_report_generator import (
    RCAReportGenerator
)


def test_rca_report_generator():

    print()
    print("=" * 60)
    print("RCA REPORT GENERATOR TEST")
    print("=" * 60)

    # -------------------------------------------------
    # Create realistic anomaly from AnomalyDetector
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Create RCA manager
    # -------------------------------------------------

    generator = (
        RCAReportGenerator()
    )

    # -------------------------------------------------
    # Generate report
    # -------------------------------------------------

    report = (
        generator.generate_report(
            anomaly
        )
    )

    # -------------------------------------------------
    # Print
    # -------------------------------------------------

    generator.print_report(
        report
    )

    # -------------------------------------------------
    # Validate report fields
    # -------------------------------------------------

    required_fields = [

        "tower_id",

        "anomaly_type",

        "severity",

        "metric",

        "value",

        "threshold",

        "event",

        "root_cause",

        "rule_based_root_cause",

        "historical_root_cause",

        "confidence",

        "evidence",

        "evidence_sources",

        "related_log_count",

        "historical_match",

        "recommended_action"
    ]

    for field in required_fields:

        assert field in report, (
            f"Missing RCA field: {field}"
        )

    # -------------------------------------------------
    # Validate values
    # -------------------------------------------------

    assert (
        report["tower_id"]
        == "Tower-001"
    )

    assert (
        report["anomaly_type"]
        == "HIGH_LATENCY"
    )

    assert (
        report["severity"]
        == "CRITICAL"
    )

    assert (
        report["root_cause"]
        == "BACKHAUL_FAILURE"
    )

    assert (
        0 <= report["confidence"] <= 1
    )

    assert (
        len(report["evidence"]) > 0
    )

    assert (
        len(
            report["evidence_sources"]
        ) > 0
    )

    assert (
        report["recommended_action"]
        != ""
    )

    print()
    print(
        "All RCA report fields validated."
    )

    print()
    print("=" * 60)
    print("ALL RCA INTEGRATION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":

    test_rca_report_generator()