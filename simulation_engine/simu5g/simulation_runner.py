"""
Simulation Runner

Main orchestration layer for the telecom RAN simulation.

Pipeline:

Scenario
    ↓
Traffic Generator
    ↓
KPI Generator
    ↓
Event Manager
    ↓
Anomaly Detection
    ↓
Network Snapshot
"""

import random
from datetime import datetime

from simulation_engine.simu5g.scenario_manager import ScenarioManager


class SimulationRunner:
    """
    Main simulation orchestrator.

    Generates tower KPIs, applies scenario-specific behavior,
    injects network events and produces a network snapshot.
    """

    def __init__(
        self,
        num_towers=10,
        seed=None,
        anomaly_detector=None,
        event_manager=None,
    ):
        """
        Parameters
        ----------
        num_towers : int
            Number of simulated towers.

        seed : int, optional
            Random seed for reproducible tests.

        anomaly_detector : object, optional
            Existing anomaly detection component.

        event_manager : object, optional
            Existing event injection component.
        """

        self.num_towers = num_towers

        self.random = random.Random(seed)

        self.scenario_manager = ScenarioManager(
            seed=seed
        )

        self.anomaly_detector = anomaly_detector
        self.event_manager = event_manager

        self.cycle = 0

        self.tower_ids = [
            f"Tower-{index:03d}"
            for index in range(1, num_towers + 1)
        ]

        self.scenario_assignments = (
            self.scenario_manager.assign_scenarios(
                self.tower_ids
            )
        )

    # ---------------------------------------------------------
    # BASE KPI GENERATION
    # ---------------------------------------------------------

    def generate_base_kpis(self):
        """
        Generate base KPI values for a tower.

        These values represent a healthy generic 5G tower.
        Scenario modifiers are applied afterwards.
        """

        return {
            "connected_users": self.random.randint(
                100, 500
            ),

            "traffic_mbps": round(
                self.random.uniform(50, 500),
                2,
            ),

            "throughput_mbps": round(
                self.random.uniform(100, 900),
                2,
            ),

            "latency_ms": round(
                self.random.uniform(5, 40),
                2,
            ),

            "packet_loss_pct": round(
                self.random.uniform(0.1, 2.0),
                2,
            ),

            "prb_utilization": round(
                self.random.uniform(20, 70),
                2,
            ),

            "signal_quality": round(
                self.random.uniform(70, 100),
                2,
            ),

            "mobility_rate": round(
                self.random.uniform(10, 50),
                2,
            ),
        }

    # ---------------------------------------------------------
    # SCENARIO GENERATION
    # ---------------------------------------------------------

    def generate_tower(self, tower_id):
        """
        Generate one complete tower state.
        """

        scenario = self.scenario_assignments[tower_id]

        base_kpis = self.generate_base_kpis()

        kpis = self.scenario_manager.apply_scenario(
            base_kpis,
            scenario,
        )

        # Keep simulated KPI values within realistic ranges.
        kpis["connected_users"] = max(
            1,
            int(kpis["connected_users"])
        )

        kpis["traffic_mbps"] = round(
            max(0, kpis["traffic_mbps"]),
            2,
        )

        kpis["throughput_mbps"] = round(
            max(0, kpis["throughput_mbps"]),
            2,
        )

        kpis["latency_ms"] = round(
            max(1, kpis["latency_ms"]),
            2,
        )

        kpis["packet_loss_pct"] = round(
            max(0, min(100, kpis["packet_loss_pct"])),
            2,
        )

        kpis["prb_utilization"] = round(
            max(0, min(100, kpis["prb_utilization"])),
            2,
        )

        kpis["signal_quality"] = round(
            max(0, min(100, kpis["signal_quality"])),
            2,
        )

        kpis["mobility_rate"] = round(
            max(0, kpis["mobility_rate"]),
            2,
        )

        tower = {
            "tower_id": tower_id,
            "scenario": scenario,
            "cycle": self.cycle,
            "timestamp": datetime.now().isoformat(),
            "kpis": kpis,
        }

        return tower

    # ---------------------------------------------------------
    # TRAFFIC
    # ---------------------------------------------------------

    def generate_traffic(self, tower):
        """
        Generate traffic-related information.

        Scenario-specific traffic is already reflected in
        the KPI values, so this method adds traffic state.
        """

        kpis = tower["kpis"]

        traffic = kpis["traffic_mbps"]

        if traffic < 100:
            traffic_state = "LOW"

        elif traffic < 300:
            traffic_state = "MEDIUM"

        elif traffic < 600:
            traffic_state = "HIGH"

        else:
            traffic_state = "VERY_HIGH"

        tower["traffic"] = {
            "traffic_mbps": traffic,
            "traffic_state": traffic_state,
        }

        return tower

    # ---------------------------------------------------------
    # EVENT INJECTION
    # ---------------------------------------------------------

    def apply_events(self, tower):
        """
        Apply event manager if one is supplied.

        The method supports several common interfaces so that
        the existing event injection implementation can be
        connected without changing this runner.
        """

        if self.event_manager is None:
            tower["event"] = None
            return tower

        # Interface 1:
        # event_manager.apply_event(tower)
        if hasattr(self.event_manager, "apply_event"):
            result = self.event_manager.apply_event(tower)

            if result is not None:
                tower = result

            return tower

        # Interface 2:
        # event_manager.inject_event(tower)
        if hasattr(self.event_manager, "inject_event"):
            result = self.event_manager.inject_event(tower)

            if result is not None:
                tower = result

            return tower

        # Interface 3:
        # event_manager.process(tower)
        if hasattr(self.event_manager, "process"):
            result = self.event_manager.process(tower)

            if result is not None:
                tower = result

            return tower

        tower["event"] = None

        return tower

    # ---------------------------------------------------------
    # ANOMALY DETECTION
    # ---------------------------------------------------------

    def detect_anomaly(self, tower):
        """
        Run the existing anomaly detector.

        Supports common detector method names.
        """

        if self.anomaly_detector is None:
            tower["anomaly"] = None
            return tower

        result = None

        if hasattr(
            self.anomaly_detector,
            "detect",
        ):
            result = self.anomaly_detector.detect(tower)

        elif hasattr(
            self.anomaly_detector,
            "detect_anomaly",
        ):
            result = self.anomaly_detector.detect_anomaly(
                tower
            )

        elif hasattr(
            self.anomaly_detector,
            "process",
        ):
            result = self.anomaly_detector.process(
                tower
            )

        if result is None:
            tower["anomaly"] = None

        elif isinstance(result, dict):
            tower["anomaly"] = result

        else:
            tower["anomaly"] = {
                "detected": bool(result)
            }

        return tower

    # ---------------------------------------------------------
    # SINGLE TOWER
    # ---------------------------------------------------------

    def simulate_tower(self, tower_id):
        """
        Simulate one tower for the current cycle.
        """

        tower = self.generate_tower(tower_id)

        tower = self.generate_traffic(tower)

        tower = self.apply_events(tower)

        tower = self.detect_anomaly(tower)

        return tower

    # ---------------------------------------------------------
    # COMPLETE CYCLE
    # ---------------------------------------------------------

    def run_cycle(self):
        """
        Run one complete simulation cycle.

        Returns
        -------
        dict
            Complete network snapshot.
        """

        self.cycle += 1

        towers = []

        for tower_id in self.tower_ids:
            tower = self.simulate_tower(
                tower_id
            )

            towers.append(tower)

        anomaly_count = 0

        for tower in towers:

            anomaly = tower.get("anomaly")

            if anomaly:

                if isinstance(anomaly, dict):

                    detected = anomaly.get(
                        "detected",
                        anomaly.get(
                            "is_anomaly",
                            True,
                        ),
                    )

                    if detected:
                        anomaly_count += 1

                else:
                    anomaly_count += 1

        snapshot = {
            "cycle": self.cycle,

            "timestamp": datetime.now().isoformat(),

            "tower_count": len(towers),

            "anomaly_count": anomaly_count,

            "towers": towers,
        }

        return snapshot

    # ---------------------------------------------------------
    # MULTIPLE CYCLES
    # ---------------------------------------------------------

    def run(self, cycles=1):
        """
        Run multiple simulation cycles.

        Parameters
        ----------
        cycles : int
            Number of cycles.

        Returns
        -------
        list
            List of network snapshots.
        """

        snapshots = []

        for _ in range(cycles):

            snapshot = self.run_cycle()

            snapshots.append(snapshot)

        return snapshots

    # ---------------------------------------------------------
    # SCENARIO INFORMATION
    # ---------------------------------------------------------

    def get_scenario_assignments(self):
        """
        Return tower-to-scenario mapping.
        """

        return self.scenario_assignments.copy()