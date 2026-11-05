from optimization_engine.load_balancing.load_balancer import LoadBalancer
from optimization_engine.load_balancing.traffic_optimizer import TrafficOptimizer
from optimization_engine.power_control.power_optimizer import PowerOptimizer
from optimization_engine.power_control.antenna_optimizer import AntennaOptimizer
from optimization_engine.coverage_optimizer.coverage_optimizer import CoverageOptimizer
from optimization_engine.coverage_optimizer.resource_allocator import ResourceAllocator


class RCAOptimizer:

    RCA_STRATEGIES = {
        "NETWORK_CONGESTION": [
            "LOAD_BALANCING",
            "TRAFFIC_OPTIMIZATION",
            "RESOURCE_ALLOCATION"
        ],

        "NETWORK_DEGRADATION": [
            "TRAFFIC_OPTIMIZATION",
            "RESOURCE_ALLOCATION"
        ],

        "RADIO_INTERFERENCE": [
            "POWER_CONTROL",
            "ANTENNA_OPTIMIZATION",
            "COVERAGE_OPTIMIZATION"
        ],

        "RADIO_DEGRADATION": [
            "POWER_CONTROL",
            "ANTENNA_OPTIMIZATION",
            "COVERAGE_OPTIMIZATION"
        ],

        "RESOURCE_CONGESTION": [
            "LOAD_BALANCING",
            "TRAFFIC_OPTIMIZATION",
            "RESOURCE_ALLOCATION"
        ],

        "PROCESSING_OVERLOAD": [
            "LOAD_BALANCING",
            "TRAFFIC_OPTIMIZATION"
        ],

        "CELL_FAILURE": [
            "COVERAGE_OPTIMIZATION",
            "RESOURCE_ALLOCATION"
        ],

        "POWER_ISSUE": [
            "POWER_CONTROL",
            "COVERAGE_OPTIMIZATION"
        ],

        "BACKHAUL_FAILURE": [
            "TRAFFIC_OPTIMIZATION",
            "LOAD_BALANCING"
        ],

        "UNKNOWN": [
            "LOAD_BALANCING",
            "TRAFFIC_OPTIMIZATION"
        ]
    }

    def __init__(self):

        self.load_balancer = LoadBalancer()
        self.traffic_optimizer = TrafficOptimizer()
        self.power_optimizer = PowerOptimizer()
        self.antenna_optimizer = AntennaOptimizer()
        self.coverage_optimizer = CoverageOptimizer()
        self.resource_allocator = ResourceAllocator()

        self.optimizers = {
            "LOAD_BALANCING": self.load_balancer,
            "TRAFFIC_OPTIMIZATION": self.traffic_optimizer,
            "POWER_CONTROL": self.power_optimizer,
            "ANTENNA_OPTIMIZATION": self.antenna_optimizer,
            "COVERAGE_OPTIMIZATION": self.coverage_optimizer,
            "RESOURCE_ALLOCATION": self.resource_allocator
        }

    def get_strategy(self, root_cause):

        return self.RCA_STRATEGIES.get(
            root_cause,
            self.RCA_STRATEGIES["UNKNOWN"]
        )

    def optimize(self, anomaly, root_cause):

        tower_id = anomaly.get(
            "tower_id",
            "UNKNOWN"
        )

        strategy = self.get_strategy(root_cause)

        tower = dict(anomaly)

        tower["tower_id"] = tower_id

        results = []

        for optimization_type in strategy:

            optimizer = self.optimizers.get(
                optimization_type
            )

            if optimizer is None:
                continue

            result = optimizer.optimize(tower)

            result["root_cause"] = root_cause

            results.append(result)

        return {
            "tower_id": tower_id,
            "root_cause": root_cause,
            "strategy": strategy,
            "optimizations": results
        }

    def optimize_rca_report(self, rca_report):

        anomaly = rca_report.get(
            "anomaly_data",
            {}
        )

        root_cause = rca_report.get(
            "root_cause",
            "UNKNOWN"
        )

        return self.optimize(
            anomaly,
            root_cause
        )