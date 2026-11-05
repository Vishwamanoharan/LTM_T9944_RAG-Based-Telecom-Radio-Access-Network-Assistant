# anomaly_detection/anomaly_detector.py

class AnomalyDetector:

    def __init__(self):

        # =============================================
        # KPI THRESHOLDS
        # =============================================

        self.latency_warning = 50
        self.latency_critical = 100

        self.packet_loss_warning = 2
        self.packet_loss_critical = 5

        self.sinr_warning = 10
        self.sinr_critical = 0

        self.throughput_warning = 100
        self.throughput_critical = 50

        self.prb_warning = 80
        self.prb_critical = 95

        self.cpu_warning = 80
        self.cpu_critical = 95

    # =================================================
    # DETECT ANOMALIES FOR ONE TOWER
    # =================================================

    def detect_tower_anomalies(
        self,
        kpi_record
    ):

        anomalies = []

        tower_id = kpi_record[
            "tower_id"
        ]

        event = kpi_record.get(
            "event",
            "NORMAL"
        )

        latency = kpi_record[
            "latency_ms"
        ]

        packet_loss = kpi_record[
            "packet_loss_pct"
        ]

        sinr = kpi_record[
            "sinr_db"
        ]

        throughput = kpi_record[
            "throughput_mbps"
        ]

        prb = kpi_record[
            "prb_utilization_pct"
        ]

        cpu = kpi_record[
            "cpu_utilization_pct"
        ]

        # =============================================
        # HIGH LATENCY
        # =============================================

        if latency >= self.latency_critical:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_LATENCY",
                "severity": "CRITICAL",
                "metric": "latency_ms",
                "value": latency,
                "threshold": self.latency_critical,
                "event": event
            })

        elif latency >= self.latency_warning:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_LATENCY",
                "severity": "WARNING",
                "metric": "latency_ms",
                "value": latency,
                "threshold": self.latency_warning,
                "event": event
            })

        # =============================================
        # HIGH PACKET LOSS
        # =============================================

        if packet_loss >= self.packet_loss_critical:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_PACKET_LOSS",
                "severity": "CRITICAL",
                "metric": "packet_loss_pct",
                "value": packet_loss,
                "threshold": self.packet_loss_critical,
                "event": event
            })

        elif packet_loss >= self.packet_loss_warning:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_PACKET_LOSS",
                "severity": "WARNING",
                "metric": "packet_loss_pct",
                "value": packet_loss,
                "threshold": self.packet_loss_warning,
                "event": event
            })

        # =============================================
        # LOW SINR
        # =============================================

        if sinr <= self.sinr_critical:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "LOW_SINR",
                "severity": "CRITICAL",
                "metric": "sinr_db",
                "value": sinr,
                "threshold": self.sinr_critical,
                "event": event
            })

        elif sinr <= self.sinr_warning:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "LOW_SINR",
                "severity": "WARNING",
                "metric": "sinr_db",
                "value": sinr,
                "threshold": self.sinr_warning,
                "event": event
            })

        # =============================================
        # LOW THROUGHPUT
        # =============================================

        if throughput <= self.throughput_critical:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "LOW_THROUGHPUT",
                "severity": "CRITICAL",
                "metric": "throughput_mbps",
                "value": throughput,
                "threshold": self.throughput_critical,
                "event": event
            })

        elif throughput <= self.throughput_warning:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "LOW_THROUGHPUT",
                "severity": "WARNING",
                "metric": "throughput_mbps",
                "value": throughput,
                "threshold": self.throughput_warning,
                "event": event
            })

        # =============================================
        # HIGH PRB UTILIZATION
        # =============================================

        if prb >= self.prb_critical:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_PRB_UTILIZATION",
                "severity": "CRITICAL",
                "metric": "prb_utilization_pct",
                "value": prb,
                "threshold": self.prb_critical,
                "event": event
            })

        elif prb >= self.prb_warning:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_PRB_UTILIZATION",
                "severity": "WARNING",
                "metric": "prb_utilization_pct",
                "value": prb,
                "threshold": self.prb_warning,
                "event": event
            })

        # =============================================
        # HIGH CPU UTILIZATION
        # =============================================

        if cpu >= self.cpu_critical:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_CPU_UTILIZATION",
                "severity": "CRITICAL",
                "metric": "cpu_utilization_pct",
                "value": cpu,
                "threshold": self.cpu_critical,
                "event": event
            })

        elif cpu >= self.cpu_warning:

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "HIGH_CPU_UTILIZATION",
                "severity": "WARNING",
                "metric": "cpu_utilization_pct",
                "value": cpu,
                "threshold": self.cpu_warning,
                "event": event
            })

        # =============================================
        # CELL OUTAGE
        # =============================================

        if event == "CELL_OUTAGE":

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "CELL_OUTAGE",
                "severity": "CRITICAL",
                "metric": "throughput_mbps",
                "value": throughput,
                "threshold": 0,
                "event": event
            })

        # =============================================
        # POWER FAILURE
        # =============================================

        if event == "POWER_FAILURE":

            anomalies.append({
                "tower_id": tower_id,
                "anomaly_type": "POWER_FAILURE",
                "severity": "CRITICAL",
                "metric": "packet_loss_pct",
                "value": packet_loss,
                "threshold": 100,
                "event": event
            })

        return anomalies

    # =================================================
    # DETECT NETWORK ANOMALIES
    # =================================================

    def detect_network_anomalies(
        self,
        kpi_data
    ):

        all_anomalies = []

        for tower in kpi_data:

            tower_anomalies = (
                self.detect_tower_anomalies(
                    tower
                )
            )

            all_anomalies.extend(
                tower_anomalies
            )

        return all_anomalies

    # =================================================
    # DISPLAY ANOMALIES
    # =================================================

    def print_anomalies(
        self,
        anomalies
    ):

        print("\n================================")
        print("ANOMALY DETECTION RESULTS")
        print("================================")

        if not anomalies:

            print(
                "No anomalies detected."
            )

            return

        for anomaly in anomalies:

            print(
                f"{anomaly['tower_id']} | "
                f"{anomaly['anomaly_type']} | "
                f"{anomaly['severity']} | "
                f"{anomaly['metric']}="
                f"{anomaly['value']} | "
                f"Event={anomaly['event']}"
            )


# =========================================================
# MAIN TEST
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

    from simulation_engine.event_generator.event_manager import (
        EventManager
    )

    # ---------------------------------------------
    # Generate towers
    # ---------------------------------------------

    towers = (
        TowerGenerator()
        .generate_towers()
    )

    # ---------------------------------------------
    # Generate traffic
    # ---------------------------------------------

    traffic = (
        TrafficGenerator()
        .generate_network_traffic(
            towers
        )
    )

    # ---------------------------------------------
    # Generate KPIs
    # ---------------------------------------------

    kpis = (
        KPIGenerator()
        .generate_network_kpis(
            traffic
        )
    )

    # ---------------------------------------------
    # Inject events
    # ---------------------------------------------

    event_manager = EventManager()

    network_data = (
        event_manager.apply_network_events(
            kpis
        )
    )

    # ---------------------------------------------
    # Detect anomalies
    # ---------------------------------------------

    detector = AnomalyDetector()

    anomalies = (
        detector.detect_network_anomalies(
            network_data
        )
    )

    # ---------------------------------------------
    # Display
    # ---------------------------------------------

    detector.print_anomalies(
        anomalies
    )