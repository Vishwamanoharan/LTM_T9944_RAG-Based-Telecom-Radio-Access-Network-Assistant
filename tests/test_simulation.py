"""
Integrated Simulation Layer Test

Tests:

    Scenario Manager
        ↓
    Simulation Runner
        ↓
    Traffic Generation
        ↓
    KPI Generation
        ↓
    Event Integration
        ↓
    Anomaly Integration
        ↓
    Multi-cycle Simulation
"""

from simulation_engine.simu5g.scenario_manager import (
    ScenarioManager,
)

from simulation_engine.simu5g.simulation_runner import (
    SimulationRunner,
)


def validate_kpis(kpis):
    """
    Validate required KPI fields.
    """

    required_fields = [
        "connected_users",
        "traffic_mbps",
        "throughput_mbps",
        "latency_ms",
        "packet_loss_pct",
        "prb_utilization",
        "signal_quality",
        "mobility_rate",
    ]

    for field in required_fields:

        assert field in kpis, (
            f"Missing KPI field: {field}"
        )

    assert kpis["connected_users"] >= 0

    assert kpis["traffic_mbps"] >= 0

    assert kpis["throughput_mbps"] >= 0

    assert kpis["latency_ms"] >= 0

    assert 0 <= kpis["packet_loss_pct"] <= 100

    assert 0 <= kpis["prb_utilization"] <= 100

    assert 0 <= kpis["signal_quality"] <= 100

    assert kpis["mobility_rate"] >= 0


def test_scenario_manager():
    """
    Test scenario assignment.
    """

    manager = ScenarioManager(seed=42)

    tower_ids = [
        f"Tower-{index:03d}"
        for index in range(1, 11)
    ]

    assignments = manager.assign_scenarios(
        tower_ids
    )

    assert len(assignments) == 10

    expected_scenarios = [
        "Urban Dense",
        "Rural",
        "Highway",
        "Airport",
        "Industrial",
        "Stadium",
    ]

    for scenario in expected_scenarios:

        assert scenario in assignments.values()

    print()
    print("Scenario assignments:")

    for tower_id, scenario in assignments.items():

        print(
            f"  {tower_id} -> {scenario}"
        )


def test_simulation_runner():

    print()
    print("=" * 60)
    print("SIMULATION LAYER INTEGRATION TEST")
    print("=" * 60)

    # --------------------------------------------------
    # Create simulation runner
    # --------------------------------------------------

    runner = SimulationRunner(
        num_towers=10,
        seed=42,
    )

    # --------------------------------------------------
    # Verify tower count
    # --------------------------------------------------

    assignments = (
        runner.get_scenario_assignments()
    )

    assert len(assignments) == 10

    print()
    print("Tower scenario mapping:")

    for tower_id, scenario in assignments.items():

        print(
            f"{tower_id} -> {scenario}"
        )

    # --------------------------------------------------
    # Run first cycle
    # --------------------------------------------------

    snapshot = runner.run_cycle()

    assert snapshot is not None

    assert snapshot["cycle"] == 1

    assert snapshot["tower_count"] == 10

    assert len(snapshot["towers"]) == 10

    print()
    print(
        f"Cycle: {snapshot['cycle']}"
    )

    print(
        f"Towers: {snapshot['tower_count']}"
    )

    print(
        f"Anomalies: {snapshot['anomaly_count']}"
    )

    # --------------------------------------------------
    # Validate every tower
    # --------------------------------------------------

    for tower in snapshot["towers"]:

        assert "tower_id" in tower

        assert "scenario" in tower

        assert "timestamp" in tower

        assert "cycle" in tower

        assert "kpis" in tower

        assert "traffic" in tower

        validate_kpis(
            tower["kpis"]
        )

    print()
    print(
        "All tower KPI validations passed."
    )

    # --------------------------------------------------
    # Verify scenarios create different behavior
    # --------------------------------------------------

    urban_tower = next(
        tower
        for tower in snapshot["towers"]
        if tower["scenario"] == "Urban Dense"
    )

    rural_tower = next(
        tower
        for tower in snapshot["towers"]
        if tower["scenario"] == "Rural"
    )

    urban_users = urban_tower[
        "kpis"
    ]["connected_users"]

    rural_users = rural_tower[
        "kpis"
    ]["connected_users"]

    assert urban_users != rural_users

    print()
    print(
        "Scenario-specific KPI behavior verified."
    )

    print(
        f"Urban Dense users: {urban_users}"
    )

    print(
        f"Rural users: {rural_users}"
    )

    # --------------------------------------------------
    # Run multiple cycles
    # --------------------------------------------------

    snapshots = runner.run(
        cycles=5
    )

    assert len(snapshots) == 5

    for index, cycle_snapshot in enumerate(
        snapshots,
        start=2,
    ):

        assert (
            cycle_snapshot["cycle"]
            == index
        )

        assert (
            cycle_snapshot["tower_count"]
            == 10
        )

        assert len(
            cycle_snapshot["towers"]
        ) == 10

    print()
    print(
        "Multi-cycle simulation passed."
    )

    # --------------------------------------------------
    # Verify KPI values change between cycles
    # --------------------------------------------------

    first_cycle = snapshot

    last_cycle = snapshots[-1]

    first_values = [
        tower["kpis"]["traffic_mbps"]
        for tower in first_cycle["towers"]
    ]

    last_values = [
        tower["kpis"]["traffic_mbps"]
        for tower in last_cycle["towers"]
    ]

    assert first_values != last_values

    print(
        "Dynamic KPI variation verified."
    )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("ALL SIMULATION TESTS PASSED")
    print("=" * 60)

if __name__ == "__main__":
    test_scenario_manager()
    test_simulation_runner()