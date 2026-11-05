class ResourceAllocator:

    def __init__(self):
        self.high_prb_threshold = 80.0
        self.critical_prb_threshold = 90.0

    def optimize(self, tower):
        tower_id = tower.get("tower_id", "UNKNOWN")

        prb = float(
            tower.get(
                "prb_utilization_pct",
                tower.get("prb_utilization", 0)
            )
        )

        if prb >= self.critical_prb_threshold:
            allocation = "MAXIMUM_ADDITIONAL_RESOURCES"
            priority = "CRITICAL"

        elif prb >= self.high_prb_threshold:
            allocation = "ADDITIONAL_PRB_RESOURCES"
            priority = "HIGH"

        else:
            allocation = "NO_ADDITIONAL_RESOURCES"
            priority = "NORMAL"

        return {
            "tower_id": tower_id,
            "optimization_type": "RESOURCE_ALLOCATION",
            "prb_utilization_pct": prb,
            "allocation": allocation,
            "priority": priority,
            "reason": (
                "Additional radio resources required"
                if prb >= self.high_prb_threshold
                else "Current resource allocation is sufficient"
            )
        }