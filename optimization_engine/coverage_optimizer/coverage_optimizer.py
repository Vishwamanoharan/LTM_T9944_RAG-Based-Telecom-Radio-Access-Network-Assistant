class CoverageOptimizer:

    def __init__(self):
        self.low_sinr_threshold = 5.0
        self.high_packet_loss_threshold = 5.0

    def optimize(self, tower):
        tower_id = tower.get("tower_id", "UNKNOWN")

        sinr = float(tower.get("sinr_db", 0))
        packet_loss = float(tower.get("packet_loss_pct", 0))

        if (
            sinr < self.low_sinr_threshold
            and packet_loss >= self.high_packet_loss_threshold
        ):
            action = "EXPAND_OR_REBALANCE_COVERAGE"
            priority = "CRITICAL"
            reason = (
                "Poor radio quality and packet delivery indicate "
                "a possible coverage problem"
            )

        elif sinr < self.low_sinr_threshold:
            action = "INVESTIGATE_COVERAGE_GAP"
            priority = "HIGH"
            reason = "Low SINR indicates possible coverage degradation"

        else:
            action = "MAINTAIN_COVERAGE"
            priority = "NORMAL"
            reason = "Coverage indicators are acceptable"

        return {
            "tower_id": tower_id,
            "optimization_type": "COVERAGE_OPTIMIZATION",
            "sinr_db": sinr,
            "packet_loss_pct": packet_loss,
            "action": action,
            "priority": priority,
            "reason": reason
        }