# simulation_engine/kpi_generator/tower_generator.py

class TowerGenerator:

    def __init__(self):

        self.regions = [
            "North",
            "South",
            "East",
            "West",
            "Central"
        ]

    # =====================================================
    # GENERATE TOWERS
    # =====================================================

    def generate_towers(
        self,
        num_towers=10
    ):

        towers = []

        for i in range(1, num_towers + 1):

            tower = {

                "tower_id":
                    f"Tower-{i:03d}",

                "site_name":
                    f"RAN_Site_{i:03d}",

                "region":
                    self.regions[
                        (i - 1) % len(self.regions)
                    ],

                "status":
                    "NORMAL"
            }

            towers.append(tower)

        return towers

    # =====================================================
    # DISPLAY TOWERS
    # =====================================================

    def print_towers(
        self,
        towers
    ):

        print("\n================================")
        print("GENERATED TOWERS")
        print("================================")

        for tower in towers:

            print(
                f"{tower['tower_id']} | "
                f"{tower['site_name']} | "
                f"{tower['region']} | "
                f"{tower['status']}"
            )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    generator = TowerGenerator()

    towers = generator.generate_towers()

    generator.print_towers(towers)