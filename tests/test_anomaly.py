# tests/test_anomaly.py

from simulation_engine.kpi_generator.tower_generator import (
    TowerGenerator
)

from simulation_engine.kpi_generator.traffic_generator import (
    TrafficGenerator
)

from simulation_engine.kpi_generator.kpi_generator import (
    KPIGenerator
)

from simulation_engine.event_generator.event_manager import (
    EventManager
)

from anomaly_detection.anomaly_engine.anomaly_detector import (
    AnomalyDetector
)


def run_simulation_cycle():

    towers = (
        TowerGenerator()
        .generate_towers(
            num_towers=10
        )
    )

    traffic = (
        TrafficGenerator()
        .generate_network_traffic(
            towers
        )
    )

    kpis = (
        KPIGenerator()
        .generate_network_kpis(
            traffic
        )
    )

    event_manager = EventManager()

    network_data = (
        event_manager.apply_network_events(
            kpis
        )
    )

    detector = AnomalyDetector()

    anomalies = (
        detector.detect_network_anomalies(
            network_data
        )
    )

    return network_data, anomalies


def test_anomaly_detection_runs():

    network_data, anomalies = (
        run_simulation_cycle()
    )

    assert len(network_data) == 10

    assert isinstance(
        anomalies,
        list
    )

    print(
        "\nAnomaly detection cycle completed."
    )

    print(
        f"Towers processed: "
        f"{len(network_data)}"
    )

    print(
        f"Anomalies detected: "
        f"{len(anomalies)}"
    )


def test_anomaly_records_are_valid():

    network_data, anomalies = (
        run_simulation_cycle()
    )

    valid_severities = {
        "WARNING",
        "CRITICAL"
    }

    for anomaly in anomalies:

        assert "tower_id" in anomaly

        assert "anomaly_type" in anomaly

        assert "severity" in anomaly

        assert "metric" in anomaly

        assert "value" in anomaly

        assert "threshold" in anomaly

        assert "event" in anomaly

        assert anomaly[
            "severity"
        ] in valid_severities

    print(
        "\nAll anomaly records have valid fields."
    )


def test_cell_outage_detection():

    towers = (
        TowerGenerator()
        .generate_towers(
            num_towers=1
        )
    )

    traffic = (
        TrafficGenerator()
        .generate_network_traffic(
            towers
        )
    )

    kpis = (
        KPIGenerator()
        .generate_network_kpis(
            traffic
        )
    )

    outage_record = dict(
        kpis[0]
    )

    outage_record[
        "event"
    ] = "CELL_OUTAGE"

    outage_record[
        "throughput_mbps"
    ] = 0

    outage_record[
        "active_users"
    ] = 0

    outage_record[
        "traffic_load_mbps"
    ] = 0

    outage_record[
        "packet_loss_pct"
    ] = 100

    detector = AnomalyDetector()

    anomalies = (
        detector.detect_tower_anomalies(
            outage_record
        )
    )

    anomaly_types = {
        anomaly[
            "anomaly_type"
        ]
        for anomaly in anomalies
    }

    assert "CELL_OUTAGE" in anomaly_types

    print(
        "\nCELL_OUTAGE detection passed."
    )


def test_power_failure_detection():

    towers = (
        TowerGenerator()
        .generate_towers(
            num_towers=1
        )
    )

    traffic = (
        TrafficGenerator()
        .generate_network_traffic(
            towers
        )
    )

    kpis = (
        KPIGenerator()
        .generate_network_kpis(
            traffic
        )
    )

    power_failure_record = dict(
        kpis[0]
    )

    power_failure_record[
        "event"
    ] = "POWER_FAILURE"

    power_failure_record[
        "packet_loss_pct"
    ] = 100

    detector = AnomalyDetector()

    anomalies = (
        detector.detect_tower_anomalies(
            power_failure_record
        )
    )

    anomaly_types = {
        anomaly[
            "anomaly_type"
        ]
        for anomaly in anomalies
    }

    assert "POWER_FAILURE" in anomaly_types

    print(
        "\nPOWER_FAILURE detection passed."
    )


def test_multiple_simulation_cycles():

    total_cycles = 10

    total_anomalies = 0

    events_detected = set()

    for cycle in range(
        total_cycles
    ):

        network_data, anomalies = (
            run_simulation_cycle()
        )

        total_anomalies += len(
            anomalies
        )

        for record in network_data:

            event = record.get(
                "event",
                "NORMAL"
            )

            if event != "NORMAL":

                events_detected.add(
                    event
                )

    assert total_anomalies > 0

    print(
        "\n================================"
    )

    print(
        "MULTI-CYCLE ANOMALY TEST"
    )

    print(
        "================================"
    )

    print(
        f"Simulation cycles: "
        f"{total_cycles}"
    )

    print(
        f"Total anomalies detected: "
        f"{total_anomalies}"
    )

    print(
        "Events observed:"
    )

    for event in sorted(
        events_detected
    ):

        print(
            f"  - {event}"
        )


if __name__ == "__main__":

    print(
        "\n================================"
    )

    print(
        "ANOMALY DETECTION TEST"
    )

    print(
        "================================"
    )

    test_anomaly_detection_runs()

    test_anomaly_records_are_valid()

    test_cell_outage_detection()

    test_power_failure_detection()

    test_multiple_simulation_cycles()

    print(
        "\n================================"
    )

    print(
        "ALL ANOMALY TESTS PASSED"
    )

    print(
        "================================"
    )