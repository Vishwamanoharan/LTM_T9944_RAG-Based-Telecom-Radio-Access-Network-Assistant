# simulation_engine/event_generator/event_manager.py

import random


class EventManager:

    def __init__(self):

        self.events = [

            "NORMAL",

            "CONGESTION",

            "INTERFERENCE",

            "BACKHAUL_FAILURE",

            "CELL_OUTAGE",

            "POWER_FAILURE",

            "HIGH_CPU_LOAD"
        ]

    # =====================================================
    # SELECT EVENT
    # =====================================================

    def generate_event(self):

        probabilities = [

            0.70,   # NORMAL

            0.10,   # CONGESTION

            0.06,   # INTERFERENCE

            0.05,   # BACKHAUL

            0.03,   # OUTAGE

            0.03,   # POWER

            0.03    # CPU
        ]

        return random.choices(
            self.events,
            weights=probabilities,
            k=1
        )[0]

    # =====================================================
    # APPLY EVENT
    # =====================================================

    def apply_event(
        self,
        kpi_record
    ):

        event = self.generate_event()

        modified = dict(kpi_record)

        modified["event"] = event

        # -------------------------------------------------
        # NORMAL
        # -------------------------------------------------

        if event == "NORMAL":

            return modified

        # -------------------------------------------------
        # CONGESTION
        # -------------------------------------------------

        if event == "CONGESTION":

            modified[
                "latency_ms"
            ] *= 2.5

            modified[
                "packet_loss_pct"
            ] *= 3

            modified[
                "prb_utilization_pct"
            ] = min(
                100,
                modified[
                    "prb_utilization_pct"
                ] + 20
            )

            modified[
                "throughput_mbps"
            ] *= 0.70

        # -------------------------------------------------
        # INTERFERENCE
        # -------------------------------------------------

        elif event == "INTERFERENCE":

            modified[
                "sinr_db"
            ] -= 10

            modified[
                "packet_loss_pct"
            ] *= 4

            modified[
                "throughput_mbps"
            ] *= 0.75

        # -------------------------------------------------
        # BACKHAUL FAILURE
        # -------------------------------------------------

        elif event == "BACKHAUL_FAILURE":

            modified[
                "latency_ms"
            ] *= 4

            modified[
                "throughput_mbps"
            ] *= 0.30

        # -------------------------------------------------
        # CELL OUTAGE
        # -------------------------------------------------

        elif event == "CELL_OUTAGE":

            modified[
                "throughput_mbps"
            ] = 0

            modified[
                "active_users"
            ] = 0

            modified[
                "traffic_load_mbps"
            ] = 0

            modified[
                "packet_loss_pct"
            ] = 100

        # -------------------------------------------------
        # POWER FAILURE
        # -------------------------------------------------

        elif event == "POWER_FAILURE":

            modified[
                "throughput_mbps"
            ] *= 0.20

            modified[
                "latency_ms"
            ] *= 5

            modified[
                "packet_loss_pct"
            ] = 100

        # -------------------------------------------------
        # HIGH CPU LOAD
        # -------------------------------------------------

        elif event == "HIGH_CPU_LOAD":

            modified[
                "cpu_utilization_pct"
            ] = min(
                100,
                modified[
                    "cpu_utilization_pct"
                ] + 30
            )

            modified[
                "latency_ms"
            ] *= 1.5

        # -------------------------------------------------
        # CLEAN VALUES
        # -------------------------------------------------

        modified[
            "latency_ms"
        ] = round(
            modified[
                "latency_ms"
            ],
            2
        )

        modified[
            "throughput_mbps"
        ] = round(
            modified[
                "throughput_mbps"
            ],
            2
        )

        modified[
            "packet_loss_pct"
        ] = round(
            modified[
                "packet_loss_pct"
            ],
            2
        )

        modified[
            "sinr_db"
        ] = round(
            modified[
                "sinr_db"
            ],
            2
        )

        modified[
            "cpu_utilization_pct"
        ] = round(
            modified[
                "cpu_utilization_pct"
            ],
            2
        )

        return modified

    # =====================================================
    # APPLY TO ENTIRE NETWORK
    # =====================================================

    def apply_network_events(
        self,
        kpi_data
    ):

        output = []

        for tower in kpi_data:

            output.append(
                self.apply_event(
                    tower
                )
            )

        return output

    # =====================================================
    # DISPLAY
    # =====================================================

    def print_events(
        self,
        network_data
    ):

        print("\n================================")
        print("NETWORK EVENTS")
        print("================================")

        for row in network_data:

            print(
                f"{row['tower_id']} | "
                f"{row['event']} | "
                f"Latency={row['latency_ms']} ms | "
                f"Throughput={row['throughput_mbps']} Mbps"
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

    from simulation_engine.kpi_generator.kpi_generator import (
        KPIGenerator
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

    event_manager = EventManager()

    network_data = (
        event_manager.apply_network_events(
            kpis
        )
    )

    event_manager.print_events(
        network_data
    )