from optimization_engine.rca_optimizer import RCAOptimizer


def main():

    print()
    print("=" * 70)
    print("RCA -> OPTIMIZATION INTEGRATION TEST")
    print("=" * 70)

    optimizer = RCAOptimizer()

    # ---------------------------------------------------------
    # TEST 1: NETWORK CONGESTION
    # ---------------------------------------------------------

    congestion_anomaly = {
        "tower_id": "Tower-001",
        "anomaly_type": "HIGH_PRB_UTILIZATION",
        "severity": "CRITICAL",
        "metric": "prb_utilization_pct",
        "value": 94.0,
        "threshold": 80.0,
        "event": "CONGESTION",
        "latency_ms": 140,
        "packet_loss_pct": 6.0,
        "sinr_db": 15.0,
        "throughput_mbps": 8.0,
        "prb_utilization_pct": 94.0,
        "cpu_utilization_pct": 75.0
    }

    result = optimizer.optimize(
        congestion_anomaly,
        "NETWORK_CONGESTION"
    )

    assert result["tower_id"] == "Tower-001"
    assert result["root_cause"] == "NETWORK_CONGESTION"

    assert "LOAD_BALANCING" in result["strategy"]
    assert "TRAFFIC_OPTIMIZATION" in result["strategy"]
    assert "RESOURCE_ALLOCATION" in result["strategy"]

    print()
    print("NETWORK_CONGESTION test passed.")
    print("Strategy:")
    for item in result["strategy"]:
        print(" -", item)

    # ---------------------------------------------------------
    # TEST 2: RADIO INTERFERENCE
    # ---------------------------------------------------------

    interference_anomaly = {
        "tower_id": "Tower-002",
        "anomaly_type": "LOW_SINR",
        "severity": "CRITICAL",
        "metric": "sinr_db",
        "value": 3.0,
        "threshold": 5.0,
        "event": "INTERFERENCE",
        "latency_ms": 80,
        "packet_loss_pct": 7.0,
        "sinr_db": 3.0,
        "throughput_mbps": 12.0,
        "prb_utilization_pct": 65.0,
        "cpu_utilization_pct": 60.0
    }

    result = optimizer.optimize(
        interference_anomaly,
        "RADIO_INTERFERENCE"
    )

    assert result["tower_id"] == "Tower-002"
    assert result["root_cause"] == "RADIO_INTERFERENCE"

    assert "POWER_CONTROL" in result["strategy"]
    assert "ANTENNA_OPTIMIZATION" in result["strategy"]
    assert "COVERAGE_OPTIMIZATION" in result["strategy"]

    print()
    print("RADIO_INTERFERENCE test passed.")
    print("Strategy:")
    for item in result["strategy"]:
        print(" -", item)

    # ---------------------------------------------------------
    # TEST 3: BACKHAUL FAILURE
    # ---------------------------------------------------------

    backhaul_anomaly = {
        "tower_id": "Tower-003",
        "anomaly_type": "HIGH_LATENCY",
        "severity": "CRITICAL",
        "metric": "latency_ms",
        "value": 180.0,
        "threshold": 100.0,
        "event": "BACKHAUL_FAILURE",
        "latency_ms": 180.0,
        "packet_loss_pct": 8.0,
        "sinr_db": 18.0,
        "throughput_mbps": 5.0,
        "prb_utilization_pct": 70.0,
        "cpu_utilization_pct": 55.0
    }

    result = optimizer.optimize(
        backhaul_anomaly,
        "BACKHAUL_FAILURE"
    )

    assert result["tower_id"] == "Tower-003"
    assert result["root_cause"] == "BACKHAUL_FAILURE"

    assert "TRAFFIC_OPTIMIZATION" in result["strategy"]
    assert "LOAD_BALANCING" in result["strategy"]

    print()
    print("BACKHAUL_FAILURE test passed.")
    print("Strategy:")
    for item in result["strategy"]:
        print(" -", item)

    # ---------------------------------------------------------
    # TEST 4: RESOURCE CONGESTION
    # ---------------------------------------------------------

    resource_anomaly = {
        "tower_id": "Tower-004",
        "anomaly_type": "HIGH_PRB_UTILIZATION",
        "severity": "WARNING",
        "metric": "prb_utilization_pct",
        "value": 86.0,
        "threshold": 80.0,
        "event": "CONGESTION",
        "latency_ms": 110,
        "packet_loss_pct": 4.0,
        "sinr_db": 12.0,
        "throughput_mbps": 15.0,
        "prb_utilization_pct": 86.0,
        "cpu_utilization_pct": 72.0
    }

    result = optimizer.optimize(
        resource_anomaly,
        "RESOURCE_CONGESTION"
    )

    assert result["tower_id"] == "Tower-004"
    assert result["root_cause"] == "RESOURCE_CONGESTION"

    assert "LOAD_BALANCING" in result["strategy"]
    assert "TRAFFIC_OPTIMIZATION" in result["strategy"]
    assert "RESOURCE_ALLOCATION" in result["strategy"]

    print()
    print("RESOURCE_CONGESTION test passed.")

    # ---------------------------------------------------------
    # TEST 5: POWER ISSUE
    # ---------------------------------------------------------

    power_anomaly = {
        "tower_id": "Tower-005",
        "anomaly_type": "POWER_FAILURE",
        "severity": "CRITICAL",
        "metric": "power",
        "value": 0,
        "threshold": 1,
        "event": "POWER_FAILURE",
        "latency_ms": 0,
        "packet_loss_pct": 100.0,
        "sinr_db": 0.0,
        "throughput_mbps": 0.0,
        "prb_utilization_pct": 0.0,
        "cpu_utilization_pct": 0.0
    }

    result = optimizer.optimize(
        power_anomaly,
        "POWER_ISSUE"
    )

    assert result["tower_id"] == "Tower-005"
    assert result["root_cause"] == "POWER_ISSUE"

    assert "POWER_CONTROL" in result["strategy"]
    assert "COVERAGE_OPTIMIZATION" in result["strategy"]

    print()
    print("POWER_ISSUE test passed.")

    # ---------------------------------------------------------
    # TEST 6: UNKNOWN ROOT CAUSE
    # ---------------------------------------------------------

    unknown_anomaly = {
        "tower_id": "Tower-006",
        "anomaly_type": "UNKNOWN",
        "severity": "WARNING",
        "metric": "unknown",
        "value": 0,
        "threshold": 0,
        "event": "NORMAL",
        "latency_ms": 50,
        "packet_loss_pct": 1.0,
        "sinr_db": 15.0,
        "throughput_mbps": 30.0,
        "prb_utilization_pct": 50.0,
        "cpu_utilization_pct": 40.0
    }

    result = optimizer.optimize(
        unknown_anomaly,
        "UNKNOWN"
    )

    assert result["tower_id"] == "Tower-006"
    assert result["root_cause"] == "UNKNOWN"

    assert len(result["strategy"]) > 0

    print()
    print("UNKNOWN root cause test passed.")

    # ---------------------------------------------------------
    # VALIDATE OUTPUT STRUCTURE
    # ---------------------------------------------------------

    print()
    print("Validating optimization output structure...")

    for optimization in result["optimizations"]:

        assert "tower_id" in optimization
        assert "optimization_type" in optimization
        assert "priority" in optimization
        assert "reason" in optimization
        assert "root_cause" in optimization

    print("Output structure validation passed.")

    # ---------------------------------------------------------
    # FINAL
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("ALL RCA -> OPTIMIZATION INTEGRATION TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()