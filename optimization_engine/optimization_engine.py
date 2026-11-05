from optimization_engine.load_balancing.load_balancer import (
    LoadBalancer
)

from optimization_engine.load_balancing.traffic_optimizer import (
    TrafficOptimizer
)

from optimization_engine.power_control.power_optimizer import (
    PowerOptimizer
)

from optimization_engine.power_control.antenna_optimizer import (
    AntennaOptimizer
)

from optimization_engine.coverage_optimizer.coverage_optimizer import (
    CoverageOptimizer
)

from optimization_engine.coverage_optimizer.resource_allocator import (
    ResourceAllocator
)


class OptimizationEngine:

    def __init__(self):

        self.load_balancer = LoadBalancer()
        self.traffic_optimizer = TrafficOptimizer()
        self.power_optimizer = PowerOptimizer()
        self.antenna_optimizer = AntennaOptimizer()
        self.coverage_optimizer = CoverageOptimizer()
        self.resource_allocator = ResourceAllocator()

    def optimize_tower(self, tower):

        results = []

        results.append(
            self.load_balancer.optimize(tower)
        )

        results.append(
            self.traffic_optimizer.optimize(tower)
        )

        results.append(
            self.power_optimizer.optimize(tower)
        )

        results.append(
            self.antenna_optimizer.optimize(tower)
        )

        results.append(
            self.coverage_optimizer.optimize(tower)
        )

        results.append(
            self.resource_allocator.optimize(tower)
        )

        return {
            "tower_id": tower.get("tower_id", "UNKNOWN"),
            "optimizations": results
        }

    def optimize_all(self, towers):

        results = []

        for tower in towers:
            results.append(
                self.optimize_tower(tower)
            )

        return results

    def get_priority_actions(self, results):

        priority_order = {
            "CRITICAL": 3,
            "HIGH": 2,
            "WARNING": 1,
            "NORMAL": 0
        }

        actions = []

        for tower_result in results:

            for optimization in tower_result["optimizations"]:

                if optimization["priority"] != "NORMAL":

                    actions.append(
                        optimization
                    )

        actions.sort(
            key=lambda item: priority_order.get(
                item.get("priority", "NORMAL"),
                0
            ),
            reverse=True
        )

        return actions