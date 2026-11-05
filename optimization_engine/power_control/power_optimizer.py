class PowerOptimizer:

    def __init__(self):
        self.low_sinr_threshold = 5.0
        self.high_sinr_threshold = 25.0

    def optimize(self, tower):
        tower_id = tower.get("tower_id", "UNKNOWN")

        sinr = float(tower.get("sinr_db", 0))

        if sinr < self.low_sinr_threshold:
            action = "INCREASE_TRANSMISSION_POWER"
            priority = "HIGH"
            reason = "Low SINR detected"

        elif sinr > self.high_sinr_threshold:
            action = "REDUCE_TRANSMISSION_POWER"
            priority = "WARNING"
            reason = "SINR is unnecessarily high"

        else:
            action = "MAINTAIN_POWER"
            priority = "NORMAL"
            reason = "SINR is within target range"

        return {
            "tower_id": tower_id,
            "optimization_type": "POWER_CONTROL",
            "sinr_db": sinr,
            "action": action,
            "priority": priority,
            "reason": reason
        }