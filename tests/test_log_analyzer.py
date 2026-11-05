# tests/test_log_analyzer.py

from rca_engine.log_analyzer.alarm_parser import (
    AlarmParser
)

from rca_engine.log_analyzer.log_analyzer import (
    LogAnalyzer
)

from rca_engine.log_analyzer.incident_matcher import (
    IncidentMatcher
)


def test_log_analysis():

    print()
    print("=" * 50)
    print("TELELOGS RCA TEST")
    print("=" * 50)

    parser = AlarmParser()

    analyzer = LogAnalyzer()

    matcher = IncidentMatcher()

    events = (
        parser.get_all_events()
    )

    print()
    print(
        f"Events discovered: {len(events)}"
    )

    for event in events[:10]:

        print(
            f" - {event}"
        )

    stats = (
        analyzer.get_log_statistics()
    )

    print()
    print(
        f"Total Logs: {stats['total_records']}"
    )

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

    related_logs = (
        analyzer.find_related_logs(
            anomaly
        )
    )

    print()
    print(
        f"Related logs found: "
        f"{len(related_logs)}"
    )

    historical = (
        matcher.get_historical_root_cause(
            anomaly
        )
    )

    print()
    print(
        f"Historical RCA Match: "
        f"{historical}"
    )

    print()
    print("=" * 50)
    print("TELELOGS RCA TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":

    test_log_analysis()