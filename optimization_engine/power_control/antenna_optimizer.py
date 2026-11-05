class AntennaOptimizer:

    def __init__(self):
        self.low_sinr_threshold = 5.0
        self.high_load_threshold = 80.0

    def optimize(self, tower):
        tower_id = tower.get("tower_id", "UNKNOWN")

        sinr = float(tower.get("sinr_db", 0))

        prb = float(
            tower.get(
                "prb_utilization_pct",
                tower.get("prb_utilization", 0)
            )
        )

        if sinr < self.low_sinr_threshold and prb >= self.high_load_threshold:
            action = "OPTIMIZE_ANTENNA_TILT_AND_AZIMUTH"
            priority = "HIGH"
            reason = (
                "Low SINR combined with high resource utilization "
                "indicates possible coverage optimization opportunity"
            )

        elif sinr < self.low_sinr_threshold:
            action = "CHECK_ANTENNA_COVERAGE"
            priority = "WARNING"
            reason = "Low SINR may indicate coverage or interference issues"

        else:
            action = "MAINTAIN_ANTENNA_CONFIGURATION"
            priority = "NORMAL"
            reason = "Antenna performance is acceptable"

        return {
            "tower_id": tower_id,
            "optimization_type": "ANTENNA_OPTIMIZATION",
            "sinr_db": sinr,
            "prb_utilization_pct": prb,
            "action": action,
            "priority": priority,
            "reason": reason
        }