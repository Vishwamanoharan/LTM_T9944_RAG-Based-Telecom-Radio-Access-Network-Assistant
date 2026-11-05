class LoadBalancer:

    def __init__(self):
        self.high_load_threshold = 80.0
        self.critical_load_threshold = 90.0

    def calculate_load(self, tower):
        return float(
            tower.get(
                "prb_utilization_pct",
                tower.get("prb_utilization", 0)
            )
        )

    def determine_action(self, load):
        if load >= self.critical_load_threshold:
            return "IMMEDIATE_TRAFFIC_OFFLOAD"

        if load >= self.high_load_threshold:
            return "TRAFFIC_OFFLOAD"

        return "NO_ACTION"

    def optimize(self, tower):
        tower_id = tower.get("tower_id", "UNKNOWN")
        load = self.calculate_load(tower)

        action = self.determine_action(load)

        return {
            "tower_id": tower_id,
            "optimization_type": "LOAD_BALANCING",
            "metric": "prb_utilization_pct",
            "current_value": load,
            "action": action,
            "priority": (
                "CRITICAL"
                if load >= self.critical_load_threshold
                else "HIGH"
                if load >= self.high_load_threshold
                else "NORMAL"
            ),
            "reason": (
                "PRB utilization is critically high"
                if load >= self.critical_load_threshold
                else "PRB utilization is high"
                if load >= self.high_load_threshold
                else "Load is within acceptable range"
            )
        }