"""
Scenario Manager for Telecom RAN Simulation

Assigns realistic network scenarios to towers and provides
scenario-specific KPI modifiers.

Scenarios:
    - Urban Dense
    - Rural
    - Highway
    - Airport
    - Industrial
    - Stadium
"""

import random


class ScenarioManager:
    """
    Manages tower scenarios and scenario-specific network behavior.
    """

    SCENARIOS = [
        "Urban Dense",
        "Rural",
        "Highway",
        "Airport",
        "Industrial",
        "Stadium",
    ]

    # Scenario-specific baseline configuration.
    #
    # Values are intentionally approximate because this is a
    # simulation layer, not a physical RF simulator.
    SCENARIO_CONFIG = {
        "Urban Dense": {
            "traffic_multiplier": 1.45,
            "user_multiplier": 1.60,
            "throughput_multiplier": 0.90,
            "latency_multiplier": 1.20,
            "packet_loss_multiplier": 1.25,
            "prb_multiplier": 1.35,
            "signal_multiplier": 0.90,
            "mobility_multiplier": 1.00,
            "congestion_probability": 0.30,
        },

        "Rural": {
            "traffic_multiplier": 0.55,
            "user_multiplier": 0.45,
            "throughput_multiplier": 0.90,
            "latency_multiplier": 1.35,
            "packet_loss_multiplier": 1.10,
            "prb_multiplier": 0.55,
            "signal_multiplier": 0.75,
            "mobility_multiplier": 0.45,
            "congestion_probability": 0.08,
        },

        "Highway": {
            "traffic_multiplier": 1.05,
            "user_multiplier": 0.95,
            "throughput_multiplier": 0.95,
            "latency_multiplier": 1.15,
            "packet_loss_multiplier": 1.20,
            "prb_multiplier": 0.90,
            "signal_multiplier": 0.88,
            "mobility_multiplier": 1.80,
            "congestion_probability": 0.15,
        },

        "Airport": {
            "traffic_multiplier": 1.35,
            "user_multiplier": 1.50,
            "throughput_multiplier": 0.95,
            "latency_multiplier": 1.10,
            "packet_loss_multiplier": 1.15,
            "prb_multiplier": 1.25,
            "signal_multiplier": 0.92,
            "mobility_multiplier": 1.20,
            "congestion_probability": 0.25,
        },

        "Industrial": {
            "traffic_multiplier": 1.10,
            "user_multiplier": 0.85,
            "throughput_multiplier": 0.85,
            "latency_multiplier": 1.25,
            "packet_loss_multiplier": 1.40,
            "prb_multiplier": 1.00,
            "signal_multiplier": 0.82,
            "mobility_multiplier": 0.55,
            "congestion_probability": 0.18,
        },

        "Stadium": {
            "traffic_multiplier": 1.80,
            "user_multiplier": 2.20,
            "throughput_multiplier": 0.80,
            "latency_multiplier": 1.35,
            "packet_loss_multiplier": 1.50,
            "prb_multiplier": 1.60,
            "signal_multiplier": 0.85,
            "mobility_multiplier": 0.90,
            "congestion_probability": 0.45,
        },
    }

    def __init__(self, seed=None):
        """
        Initialize the scenario manager.

        Parameters
        ----------
        seed : int, optional
            Random seed for reproducible testing.
        """

        self.random = random.Random(seed)

    def assign_scenarios(self, tower_ids):
        """
        Assign scenarios to towers.

        The first six towers receive the six primary scenarios.
        Remaining towers cycle through the scenario list.

        Parameters
        ----------
        tower_ids : list
            Tower identifiers.

        Returns
        -------
        dict
            Mapping of tower_id -> scenario.
        """

        assignments = {}

        for index, tower_id in enumerate(tower_ids):
            scenario = self.SCENARIOS[index % len(self.SCENARIOS)]
            assignments[tower_id] = scenario

        return assignments

    def get_scenario(self, tower_id, assignments):
        """
        Return the scenario assigned to a tower.
        """

        return assignments.get(tower_id)

    def get_config(self, scenario):
        """
        Return configuration for a scenario.
        """

        if scenario not in self.SCENARIO_CONFIG:
            raise ValueError(
                f"Unknown scenario: {scenario}"
            )

        return self.SCENARIO_CONFIG[scenario].copy()

    def get_random_event_probability(self, scenario):
        """
        Return probability of congestion/event pressure
        for a scenario.
        """

        config = self.get_config(scenario)

        return config["congestion_probability"]

    def apply_scenario(self, base_kpis, scenario):
        """
        Apply scenario-specific modifiers to base KPI values.

        Parameters
        ----------
        base_kpis : dict
            Base KPI dictionary.

        scenario : str
            Scenario name.

        Returns
        -------
        dict
            Modified KPI dictionary.
        """

        config = self.get_config(scenario)

        kpis = base_kpis.copy()

        # Traffic / users
        if "traffic" in kpis:
            kpis["traffic"] *= config["traffic_multiplier"]

        if "traffic_load" in kpis:
            kpis["traffic_load"] *= config["traffic_multiplier"]

        if "connected_users" in kpis:
            kpis["connected_users"] *= config["user_multiplier"]

        if "users" in kpis:
            kpis["users"] *= config["user_multiplier"]

        # Throughput
        if "throughput" in kpis:
            kpis["throughput"] *= config["throughput_multiplier"]

        if "throughput_mbps" in kpis:
            kpis["throughput_mbps"] *= config["throughput_multiplier"]

        # Latency
        if "latency" in kpis:
            kpis["latency"] *= config["latency_multiplier"]

        if "latency_ms" in kpis:
            kpis["latency_ms"] *= config["latency_multiplier"]

        # Packet loss
        if "packet_loss" in kpis:
            kpis["packet_loss"] *= config["packet_loss_multiplier"]

        if "packet_loss_pct" in kpis:
            kpis["packet_loss_pct"] *= config["packet_loss_multiplier"]

        # PRB utilization
        if "prb_utilization" in kpis:
            kpis["prb_utilization"] *= config["prb_multiplier"]

        if "prb_usage" in kpis:
            kpis["prb_usage"] *= config["prb_multiplier"]

        # Signal quality
        if "signal_quality" in kpis:
            kpis["signal_quality"] *= config["signal_multiplier"]

        if "rsrp" in kpis:
            kpis["rsrp"] *= config["signal_multiplier"]

        # Mobility
        if "mobility" in kpis:
            kpis["mobility"] *= config["mobility_multiplier"]

        if "mobility_rate" in kpis:
            kpis["mobility_rate"] *= config["mobility_multiplier"]

        return kpis

    def add_scenario_metadata(self, tower, scenario):
        """
        Add scenario information to a tower record.
        """

        tower["scenario"] = scenario

        config = self.get_config(scenario)

        tower["scenario_config"] = config

        return tower