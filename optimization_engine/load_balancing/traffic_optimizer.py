class TrafficOptimizer:

    def __init__(self):
        self.high_latency_threshold = 100.0
        self.high_packet_loss_threshold = 5.0
        self.low_throughput_threshold = 10.0

    def optimize(self, tower):
        tower_id = tower.get("tower_id", "UNKNOWN")

        latency = float(tower.get("latency_ms", 0))
        packet_loss = float(tower.get("packet_loss_pct", 0))
        throughput = float(tower.get("throughput_mbps", 0))

        actions = []

        if latency >= self.high_latency_threshold:
            actions.append("STEER_TRAFFIC_TO_NEIGHBORING_CELL")

        if packet_loss >= self.high_packet_loss_threshold:
            actions.append("REDUCE_TRAFFIC_LOAD")

        if throughput < self.low_throughput_threshold:
            actions.append("CHECK_BACKHAUL_CAPACITY")

        if not actions:
            actions.append("NO_ACTION")

        priority = "NORMAL"

        if latency >= self.high_latency_threshold:
            priority = "HIGH"

        if packet_loss >= self.high_packet_loss_threshold:
            priority = "CRITICAL"

        return {
            "tower_id": tower_id,
            "optimization_type": "TRAFFIC_OPTIMIZATION",
            "latency_ms": latency,
            "packet_loss_pct": packet_loss,
            "throughput_mbps": throughput,
            "actions": actions,
            "priority": priority,
            "reason": (
                "Traffic steering recommended because "
                "network performance degradation was detected"
                if actions != ["NO_ACTION"]
                else "Traffic performance is within acceptable limits"
            )
        }