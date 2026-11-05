from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_ROOT = (
    PROJECT_ROOT
    / "data"
    / "simulation"
)

KPI_FILE = (
    DATA_ROOT
    / "kpi_snapshots"
    / "live_kpis.csv"
)

HISTORY_FILE = (
    DATA_ROOT
    / "tower_history"
    / "tower_status.csv"
)

EVENT_FILE = (
    DATA_ROOT
    / "events"
    / "events.csv"
)


REQUIRED_KPI_COLUMNS = [

    "timestamp",

    "tower_id",

    "connected_users",

    "traffic_mbps",

    "throughput_mbps",

    "latency_ms",

    "packet_loss_pct",

    "prb_utilization_pct",

    "sinr_db",

    "rsrp_dbm",

    "cpu_utilization_pct",

    "signal_quality",

    "status"
]


def main():

    print()
    print("=" * 70)
    print("TELECOM RAN DASHBOARD TEST")
    print("=" * 70)

    # -----------------------------------------------------
    # DATA DIRECTORIES
    # -----------------------------------------------------

    print()
    print("Checking simulation directories...")

    assert DATA_ROOT.exists()

    assert (
        KPI_FILE.parent.exists()
    )

    assert (
        HISTORY_FILE.parent.exists()
    )

    assert (
        EVENT_FILE.parent.exists()
    )

    print(
        "Simulation directories validation passed."
    )

    # -----------------------------------------------------
    # KPI FILE
    # -----------------------------------------------------

    print()
    print("Checking live KPI data...")

    assert KPI_FILE.exists(), (
        "live_kpis.csv not found. "
        "Run the dashboard once first."
    )

    kpi_data = pd.read_csv(
        KPI_FILE
    )

    assert not kpi_data.empty

    print(
        f"Towers found: {len(kpi_data)}"
    )

    # -----------------------------------------------------
    # KPI COLUMNS
    # -----------------------------------------------------

    print()
    print("Checking KPI columns...")

    missing_columns = [

        column

        for column in REQUIRED_KPI_COLUMNS

        if column not in kpi_data.columns
    ]

    assert not missing_columns, (
        f"Missing KPI columns: "
        f"{missing_columns}"
    )

    print(
        "KPI column validation passed."
    )

    # -----------------------------------------------------
    # TOWER COUNT
    # -----------------------------------------------------

    print()
    print("Checking tower data...")

    assert len(kpi_data) >= 1

    assert (
        kpi_data["tower_id"]
        .notna()
        .all()
    )

    print(
        "Tower data validation passed."
    )

    # -----------------------------------------------------
    # NUMERIC KPI VALIDATION
    # -----------------------------------------------------

    print()
    print("Checking KPI values...")

    numeric_columns = [

        "connected_users",

        "traffic_mbps",

        "throughput_mbps",

        "latency_ms",

        "packet_loss_pct",

        "prb_utilization_pct",

        "sinr_db",

        "rsrp_dbm",

        "cpu_utilization_pct"
    ]

    for column in numeric_columns:

        assert pd.api.types.is_numeric_dtype(
            kpi_data[column]
        )

    assert (
        kpi_data[
            "prb_utilization_pct"
        ]
        .between(0, 100)
        .all()
    )

    assert (
        kpi_data[
            "cpu_utilization_pct"
        ]
        .between(0, 100)
        .all()
    )

    assert (
        kpi_data[
            "packet_loss_pct"
        ]
        >= 0
    ).all()

    assert (
        kpi_data[
            "latency_ms"
        ]
        >= 0
    ).all()

    print(
        "KPI value validation passed."
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    print()
    print("Checking tower status...")

    valid_statuses = {
        "HEALTHY",
        "WARNING",
        "CRITICAL"
    }

    actual_statuses = set(
        kpi_data[
            "status"
        ].dropna().unique()
    )

    assert actual_statuses.issubset(
        valid_statuses
    )

    print(
        "Tower status validation passed."
    )

    # -----------------------------------------------------
    # HISTORY FILE
    # -----------------------------------------------------

    print()
    print("Checking tower history...")

    assert HISTORY_FILE.exists()

    history = pd.read_csv(
        HISTORY_FILE
    )

    assert not history.empty

    assert (
        "tower_id"
        in history.columns
    )

    print(
        "Tower history validation passed."
    )

    # -----------------------------------------------------
    # EVENTS
    # -----------------------------------------------------

    print()
    print("Checking event data...")

    if EVENT_FILE.exists():

        events = pd.read_csv(
            EVENT_FILE
        )

        if not events.empty:

            required_event_columns = {

                "timestamp",

                "tower_id",

                "event_type",

                "severity",

                "description"
            }

            assert required_event_columns.issubset(
                set(events.columns)
            )

            print(
                f"Events found: {len(events)}"
            )

        else:

            print(
                "Event file exists but "
                "currently contains no events."
            )

    else:

        print(
            "No event file generated yet."
        )

    # -----------------------------------------------------
    # FINAL
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("ALL DASHBOARD DATA TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()