# simulation_engine/kpi_generator/kpi_generator.py

import random


class KPIGenerator:

    def __init__(self):

        pass

    # =====================================================
    # GENERATE KPI FOR ONE TOWER
    # =====================================================

    def generate_tower_kpis(
        self,
        traffic_data
    ):

        active_users = traffic_data[
            "active_users"
        ]

        traffic_load = traffic_data[
            "traffic_load_mbps"
        ]

        # ---------------------------------------------
        # PRB UTILIZATION
        # ---------------------------------------------

        prb_utilization = min(
            100,
            round(
                active_users / 5 +
                random.uniform(-5, 5),
                2
            )
        )

        # ---------------------------------------------
        # LATENCY
        # ---------------------------------------------

        latency_ms = round(

            5 +

            (prb_utilization / 100) * 40 +

            random.uniform(0, 5),

            2
        )

        # ---------------------------------------------
        # THROUGHPUT
        # ---------------------------------------------

        throughput_mbps = round(

            traffic_load *

            random.uniform(
                0.75,
                0.95
            ),

            2
        )

        # ---------------------------------------------
        # PACKET LOSS
        # ---------------------------------------------

        packet_loss_pct = round(

            max(
                0,
                (
                    prb_utilization - 75
                ) / 10
            )

            +

            random.uniform(
                0,
                0.5
            ),

            2
        )

        # ---------------------------------------------
        # SINR
        # ---------------------------------------------

        sinr_db = round(

            30 -

            (
                prb_utilization / 5
            )

            +

            random.uniform(
                -2,
                2
            ),

            2
        )

        # ---------------------------------------------
        # RSRP
        # ---------------------------------------------

        rsrp_dbm = round(

            -75 -

            (
                prb_utilization / 3
            )

            +

            random.uniform(
                -3,
                3
            ),

            2
        )

        # ---------------------------------------------
        # CPU UTILIZATION
        # ---------------------------------------------

        cpu_utilization_pct = round(

            min(
                100,

                prb_utilization *

                random.uniform(
                    0.8,
                    1.1
                )
            ),

            2
        )

        return {

            "tower_id":
                traffic_data["tower_id"],

            "active_users":
                active_users,

            "traffic_load_mbps":
                traffic_load,

            "prb_utilization_pct":
                prb_utilization,

            "latency_ms":
                latency_ms,

            "throughput_mbps":
                throughput_mbps,

            "packet_loss_pct":
                packet_loss_pct,

            "sinr_db":
                sinr_db,

            "rsrp_dbm":
                rsrp_dbm,

            "cpu_utilization_pct":
                cpu_utilization_pct
        }

    # =====================================================
    # GENERATE NETWORK KPIS
    # =====================================================

    def generate_network_kpis(
        self,
        traffic_data
    ):

        kpi_data = []

        for tower in traffic_data:

            kpi = self.generate_tower_kpis(
                tower
            )

            kpi_data.append(
                kpi
            )

        return kpi_data

    # =====================================================
    # DISPLAY
    # =====================================================

    def print_kpis(
        self,
        kpi_data
    ):

        print("\n================================")
        print("NETWORK KPIs")
        print("================================")

        for row in kpi_data:

            print(
                f"{row['tower_id']} | "
                f"PRB={row['prb_utilization_pct']}% | "
                f"Latency={row['latency_ms']} ms | "
                f"Throughput={row['throughput_mbps']} Mbps | "
                f"PacketLoss={row['packet_loss_pct']}% | "
                f"SINR={row['sinr_db']} dB"
            )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    from simulation_engine.kpi_generator.tower_generator import (
        TowerGenerator
    )

    from simulation_engine.kpi_generator.traffic_generator import (
        TrafficGenerator
    )

    towers = (
        TowerGenerator()
        .generate_towers()
    )

    traffic = (
        TrafficGenerator()
        .generate_network_traffic(
            towers
        )
    )

    kpis = (
        KPIGenerator()
        .generate_network_kpis(
            traffic
        )
    )

    KPIGenerator().print_kpis(
        kpis
    )