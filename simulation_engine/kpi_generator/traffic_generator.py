# simulation_engine/kpi_generator/traffic_generator.py

import random
from datetime import datetime


class TrafficGenerator:

    def __init__(self):

        self.min_users = 50
        self.max_users = 500

    # =====================================================
    # HOURLY TRAFFIC MULTIPLIER
    # =====================================================

    def get_hour_multiplier(self, hour):

        # Night

        if 0 <= hour < 6:
            return 0.30

        # Morning

        elif 6 <= hour < 10:
            return 0.70

        # Day

        elif 10 <= hour < 17:
            return 1.00

        # Busy Hour

        elif 17 <= hour < 22:
            return 1.50

        # Late Evening

        return 0.60

    # =====================================================
    # GENERATE TRAFFIC FOR ONE TOWER
    # =====================================================

    def generate_tower_traffic(
        self,
        tower_id
    ):

        current_hour = datetime.now().hour

        multiplier = self.get_hour_multiplier(
            current_hour
        )

        base_users = random.randint(
            self.min_users,
            self.max_users
        )

        active_users = int(
            base_users * multiplier
        )

        traffic_load_mbps = round(
            active_users *
            random.uniform(
                1.5,
                5.0
            ),
            2
        )

        return {

            "tower_id":
                tower_id,

            "active_users":
                active_users,

            "traffic_load_mbps":
                traffic_load_mbps
        }

    # =====================================================
    # GENERATE ALL TOWERS
    # =====================================================

    def generate_network_traffic(
        self,
        towers
    ):

        traffic_data = []

        for tower in towers:

            traffic = (
                self.generate_tower_traffic(
                    tower["tower_id"]
                )
            )

            traffic_data.append(
                traffic
            )

        return traffic_data

    # =====================================================
    # DISPLAY
    # =====================================================

    def print_traffic(
        self,
        traffic_data
    ):

        print("\n================================")
        print("NETWORK TRAFFIC")
        print("================================")

        for row in traffic_data:

            print(
                f"{row['tower_id']} | "
                f"Users={row['active_users']} | "
                f"Traffic={row['traffic_load_mbps']} Mbps"
            )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    from simulation_engine.kpi_generator.tower_generator import (
        TowerGenerator
    )

    tower_generator = TowerGenerator()

    towers = (
        tower_generator.generate_towers()
    )

    traffic_generator = TrafficGenerator()

    traffic_data = (
        traffic_generator.generate_network_traffic(
            towers
        )
    )

    traffic_generator.print_traffic(
        traffic_data
    )