from optimization_engine.optimization_engine import (
    OptimizationEngine
)


def main():

    print()
    print("=" * 60)
    print("OPTIMIZATION ENGINE TEST")
    print("=" * 60)

    towers = [
        {
            "tower_id": "Tower-001",
            "latency_ms": 180,
            "packet_loss_pct": 8.5,
            "sinr_db": 3.0,
            "throughput_mbps": 6.0,
            "prb_utilization_pct": 94.0,
            "cpu_utilization_pct": 91.0
        },
        {
            "tower_id": "Tower-002",
            "latency_ms": 60,
            "packet_loss_pct": 1.2,
            "sinr_db": 15.0,
            "throughput_mbps": 35.0,
            "prb_utilization_pct": 55.0,
            "cpu_utilization_pct": 50.0
        }
    ]

    engine = OptimizationEngine()

    results = engine.optimize_all(towers)

    print()
    print("Towers processed:", len(results))

    assert len(results) == 2

    for result in results:

        print()
        print("Tower:", result["tower_id"])

        assert "tower_id" in result
        assert "optimizations" in result

        assert len(result["optimizations"]) == 6

        for optimization in result["optimizations"]:

            assert "tower_id" in optimization
            assert "optimization_type" in optimization
            assert "priority" in optimization
            assert "reason" in optimization

            print(
                f"  {optimization['optimization_type']}: "
                f"{optimization['priority']}"
            )

    priority_actions = engine.get_priority_actions(
        results
    )

    print()
    print(
        "Priority optimization actions:",
        len(priority_actions)
    )

    assert len(priority_actions) > 0

    print()
    print("Top priority actions:")

    for action in priority_actions[:5]:

        print(
            f"  {action['tower_id']} | "
            f"{action['optimization_type']} | "
            f"{action['priority']} | "
            f"{action.get('action', action.get('allocation', 'N/A'))}"
        )

    tower1_actions = [
        item
        for item in results[0]["optimizations"]
        if item["priority"] in ["CRITICAL", "HIGH"]
    ]

    assert len(tower1_actions) > 0

    print()
    print("=" * 60)
    print("ALL OPTIMIZATION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()