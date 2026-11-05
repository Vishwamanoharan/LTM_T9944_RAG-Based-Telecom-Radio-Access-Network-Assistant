import os
import sys
import time
import random
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# RAG + LLM
# ============================================================

RAG_AVAILABLE = False

try:
    from llm.inference_engine.response_generator import ResponseGenerator
    RAG_AVAILABLE = True
except Exception:
    RAG_AVAILABLE = False


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="Telecom RAN AI Assistant",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DARK UI
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0e1117;
        color: white;
    }

    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .sub-header {
        color: #9aa4b2;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .status-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        text-align: center;
    }

    .metric-title {
        color: #9aa4b2;
        font-size: 0.85rem;
    }

    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
    }

    .normal-text {
        color: #2ecc71;
        font-weight: 600;
    }

    .warning-text {
        color: #f1c40f;
        font-weight: 600;
    }

    .critical-text {
        color: #e74c3c;
        font-weight: 600;
    }

    .pipeline-box {
        padding: 12px;
        border-radius: 8px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)

SIMULATION_DIR = os.path.join(
    DATA_DIR,
    "simulation"
)

KPI_DIR = os.path.join(
    SIMULATION_DIR,
    "kpi_snapshots"
)

HISTORY_DIR = os.path.join(
    SIMULATION_DIR,
    "tower_history"
)

EVENT_DIR = os.path.join(
    SIMULATION_DIR,
    "events"
)

os.makedirs(KPI_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)
os.makedirs(EVENT_DIR, exist_ok=True)


LIVE_KPI_FILE = os.path.join(
    KPI_DIR,
    "live_kpis.csv"
)

TOWER_HISTORY_FILE = os.path.join(
    HISTORY_DIR,
    "tower_status.csv"
)

EVENT_FILE = os.path.join(
    EVENT_DIR,
    "events.csv"
)


# ============================================================
# TOWER LOCATIONS
# ============================================================

TOWER_LOCATIONS = {
    "TOWER-001": (17.3850, 78.4867),
    "TOWER-002": (17.3950, 78.5000),
    "TOWER-003": (17.3700, 78.4800),
    "TOWER-004": (17.4100, 78.4700),
    "TOWER-005": (17.3600, 78.5100),
    "TOWER-006": (17.4000, 78.5200),
    "TOWER-007": (17.3500, 78.4900),
    "TOWER-008": (17.4200, 78.5000),
    "TOWER-009": (17.3750, 78.5300),
    "TOWER-010": (17.4300, 78.4800),
}

TOWER_IDS = list(TOWER_LOCATIONS.keys())


# ============================================================
# KPI COLUMNS
# ============================================================

KPI_COLUMNS = [
    "timestamp",
    "tower_id",
    "connected_users",
    "traffic_mbps",
    "throughput_mbps",
    "latency_ms",
    "packet_loss_pct",
    "prb_utilization_pct",
    "sinr_db",
    "rsrp_dbm",
    "cpu_utilization_pct",
    "signal_quality",
    "status"
]


# ============================================================
# KPI THRESHOLDS
# ============================================================

THRESHOLDS = {

    "throughput_mbps": {
        "warning": 50,
        "critical": 30
    },

    "latency_ms": {
        "warning": 50,
        "critical": 75
    },

    "packet_loss_pct": {
        "warning": 2,
        "critical": 5
    },

    "prb_utilization_pct": {
        "warning": 80,
        "critical": 95
    },

    "sinr_db": {
        "warning": 5,
        "critical": 0
    },

    "rsrp_dbm": {
        "warning": -105,
        "critical": -115
    },

    "cpu_utilization_pct": {
        "warning": 85,
        "critical": 95
    }
}


# ============================================================
# SESSION STATE
# ============================================================

if "simulation_cycle" not in st.session_state:
    st.session_state.simulation_cycle = 0

if "last_update" not in st.session_state:
    st.session_state.last_update = None

if "current_kpis" not in st.session_state:
    st.session_state.current_kpis = pd.DataFrame()

if "current_anomalies" not in st.session_state:
    st.session_state.current_anomalies = []

if "current_rca" not in st.session_state:
    st.session_state.current_rca = []

if "current_optimization" not in st.session_state:
    st.session_state.current_optimization = []

if "selected_tower" not in st.session_state:
    st.session_state.selected_tower = TOWER_IDS[0]

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True

if "refresh_seconds" not in st.session_state:
    st.session_state.refresh_seconds = 8

if "last_ai_answer" not in st.session_state:
    st.session_state.last_ai_answer = ""


# ============================================================
# BASELINES
# ============================================================

BASELINES = {}

for tower_id in TOWER_IDS:

    BASELINES[tower_id] = {
        "connected_users": random.randint(50, 180),
        "traffic_mbps": random.uniform(80, 300),
        "throughput_mbps": random.uniform(70, 180),
        "latency_ms": random.uniform(15, 40),
        "packet_loss_pct": random.uniform(0.1, 1.2),
        "prb_utilization_pct": random.uniform(40, 75),
        "sinr_db": random.uniform(8, 20),
        "rsrp_dbm": random.uniform(-95, -75),
        "cpu_utilization_pct": random.uniform(35, 75)
    }


# ============================================================
# STATUS CALCULATION
# ============================================================

def calculate_status(row):

    critical = False
    warning = False

    if row["throughput_mbps"] < THRESHOLDS["throughput_mbps"]["critical"]:
        critical = True

    elif row["throughput_mbps"] < THRESHOLDS["throughput_mbps"]["warning"]:
        warning = True


    if row["latency_ms"] > THRESHOLDS["latency_ms"]["critical"]:
        critical = True

    elif row["latency_ms"] > THRESHOLDS["latency_ms"]["warning"]:
        warning = True


    if row["packet_loss_pct"] > THRESHOLDS["packet_loss_pct"]["critical"]:
        critical = True

    elif row["packet_loss_pct"] > THRESHOLDS["packet_loss_pct"]["warning"]:
        warning = True


    if row["prb_utilization_pct"] > THRESHOLDS["prb_utilization_pct"]["critical"]:
        critical = True

    elif row["prb_utilization_pct"] > THRESHOLDS["prb_utilization_pct"]["warning"]:
        warning = True


    if row["sinr_db"] < THRESHOLDS["sinr_db"]["critical"]:
        critical = True

    elif row["sinr_db"] < THRESHOLDS["sinr_db"]["warning"]:
        warning = True


    if row["rsrp_dbm"] < THRESHOLDS["rsrp_dbm"]["critical"]:
        critical = True

    elif row["rsrp_dbm"] < THRESHOLDS["rsrp_dbm"]["warning"]:
        warning = True


    if row["cpu_utilization_pct"] > THRESHOLDS["cpu_utilization_pct"]["critical"]:
        critical = True

    elif row["cpu_utilization_pct"] > THRESHOLDS["cpu_utilization_pct"]["warning"]:
        warning = True


    if critical:
        return "Critical"

    if warning:
        return "Warning"

    return "Normal"


# ============================================================
# GENERATE TOWER KPI
# ============================================================

def generate_tower_kpi(tower_id):

    baseline = BASELINES[tower_id]

    connected_users = max(
        1,
        baseline["connected_users"] + random.randint(-20, 30)
    )

    traffic = max(
        1,
        baseline["traffic_mbps"] + random.uniform(-30, 50)
    )

    throughput = max(
        1,
        baseline["throughput_mbps"] + random.uniform(-25, 25)
    )

    latency = max(
        1,
        baseline["latency_ms"] + random.uniform(-10, 15)
    )

    packet_loss = max(
        0,
        baseline["packet_loss_pct"] + random.uniform(-0.5, 1.0)
    )

    prb = min(
        100,
        max(
            1,
            baseline["prb_utilization_pct"] + random.uniform(-10, 15)
        )
    )

    sinr = (
        baseline["sinr_db"]
        + random.uniform(-3, 3)
    )

    rsrp = (
        baseline["rsrp_dbm"]
        + random.uniform(-5, 5)
    )

    cpu = min(
        100,
        max(
            1,
            baseline["cpu_utilization_pct"] + random.uniform(-8, 10)
        )
    )


    # --------------------------------------------------------
    # RANDOM EVENTS
    # --------------------------------------------------------

    event_probability = random.random()

    if event_probability < 0.05:

        # Congestion

        connected_users += random.randint(80, 150)
        traffic += random.uniform(100, 200)
        throughput *= random.uniform(0.35, 0.65)
        latency += random.uniform(40, 80)
        packet_loss += random.uniform(2, 5)
        prb += random.uniform(15, 25)


    elif event_probability < 0.09:

        # Interference

        sinr -= random.uniform(8, 15)
        packet_loss += random.uniform(2, 6)
        throughput *= random.uniform(0.4, 0.7)


    elif event_probability < 0.12:

        # Cell outage

        throughput = random.uniform(0, 10)
        connected_users = random.randint(0, 10)
        latency = random.uniform(80, 150)
        packet_loss = random.uniform(5, 15)
        rsrp = random.uniform(-125, -115)


    elif event_probability < 0.15:

        # Power failure

        throughput = random.uniform(5, 25)
        rsrp = random.uniform(-125, -110)
        sinr = random.uniform(-5, 4)
        cpu = random.uniform(5, 25)


    elif event_probability < 0.18:

        # Backhaul failure

        throughput *= random.uniform(0.3, 0.6)
        latency += random.uniform(70, 120)
        packet_loss += random.uniform(3, 8)


    elif event_probability < 0.21:

        # High CPU

        cpu = random.uniform(90, 100)
        latency += random.uniform(20, 40)


    row = {

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "tower_id": tower_id,

        "connected_users": int(
            connected_users
        ),

        "traffic_mbps": round(
            traffic,
            2
        ),

        "throughput_mbps": round(
            throughput,
            2
        ),

        "latency_ms": round(
            latency,
            2
        ),

        "packet_loss_pct": round(
            packet_loss,
            2
        ),

        "prb_utilization_pct": round(
            prb,
            2
        ),

        "sinr_db": round(
            sinr,
            2
        ),

        "rsrp_dbm": round(
            rsrp,
            2
        ),

        "cpu_utilization_pct": round(
            cpu,
            2
        )
    }


    # --------------------------------------------------------
    # SIGNAL QUALITY
    # --------------------------------------------------------

    if row["sinr_db"] >= 10:

        signal_quality = "Good"

    elif row["sinr_db"] >= 5:

        signal_quality = "Fair"

    else:

        signal_quality = "Poor"


    row["signal_quality"] = signal_quality

    row["status"] = calculate_status(row)

    return row


# ============================================================
# APPEND HISTORY
# ============================================================

def append_to_history(df):

    try:

        df.to_csv(
            LIVE_KPI_FILE,
            index=False
        )


        if os.path.exists(
            TOWER_HISTORY_FILE
        ):

            existing = pd.read_csv(
                TOWER_HISTORY_FILE
            )

            combined = pd.concat(
                [existing, df],
                ignore_index=True
            )

        else:

            combined = df.copy()


        combined.to_csv(
            TOWER_HISTORY_FILE,
            index=False
        )

    except Exception:

        pass


# ============================================================
# GENERATE NETWORK CYCLE
# ============================================================

def generate_network_cycle():

    rows = []

    for tower_id in TOWER_IDS:

        rows.append(
            generate_tower_kpi(tower_id)
        )

    df = pd.DataFrame(rows)

    append_to_history(df)

    st.session_state.current_kpis = df

    st.session_state.simulation_cycle += 1

    st.session_state.last_update = datetime.now()

    return df


# ============================================================
# ANOMALY CREATION
# ============================================================

def create_anomaly(
    tower_id,
    anomaly_type,
    severity,
    metric,
    value,
    threshold
):

    return {

        "tower_id": tower_id,

        "anomaly_type": anomaly_type,

        "severity": severity,

        "metric": metric,

        "value": value,

        "threshold": threshold,

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


# ============================================================
# ANOMALY DETECTION
# ============================================================

def detect_anomalies(df):

    anomalies = []

    for _, row in df.iterrows():

        tower_id = row["tower_id"]


        # HIGH LATENCY

        if row["latency_ms"] > THRESHOLDS["latency_ms"]["critical"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_LATENCY",
                    "CRITICAL",
                    "latency_ms",
                    row["latency_ms"],
                    THRESHOLDS["latency_ms"]["critical"]
                )
            )

        elif row["latency_ms"] > THRESHOLDS["latency_ms"]["warning"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_LATENCY",
                    "WARNING",
                    "latency_ms",
                    row["latency_ms"],
                    THRESHOLDS["latency_ms"]["warning"]
                )
            )


        # HIGH PACKET LOSS

        if row["packet_loss_pct"] > THRESHOLDS["packet_loss_pct"]["critical"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_PACKET_LOSS",
                    "CRITICAL",
                    "packet_loss_pct",
                    row["packet_loss_pct"],
                    THRESHOLDS["packet_loss_pct"]["critical"]
                )
            )

        elif row["packet_loss_pct"] > THRESHOLDS["packet_loss_pct"]["warning"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_PACKET_LOSS",
                    "WARNING",
                    "packet_loss_pct",
                    row["packet_loss_pct"],
                    THRESHOLDS["packet_loss_pct"]["warning"]
                )
            )


        # LOW SINR

        if row["sinr_db"] < THRESHOLDS["sinr_db"]["critical"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "LOW_SINR",
                    "CRITICAL",
                    "sinr_db",
                    row["sinr_db"],
                    THRESHOLDS["sinr_db"]["critical"]
                )
            )

        elif row["sinr_db"] < THRESHOLDS["sinr_db"]["warning"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "LOW_SINR",
                    "WARNING",
                    "sinr_db",
                    row["sinr_db"],
                    THRESHOLDS["sinr_db"]["warning"]
                )
            )


        # LOW RSRP

        if row["rsrp_dbm"] < THRESHOLDS["rsrp_dbm"]["critical"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "LOW_RSRP",
                    "CRITICAL",
                    "rsrp_dbm",
                    row["rsrp_dbm"],
                    THRESHOLDS["rsrp_dbm"]["critical"]
                )
            )

        elif row["rsrp_dbm"] < THRESHOLDS["rsrp_dbm"]["warning"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "LOW_RSRP",
                    "WARNING",
                    "rsrp_dbm",
                    row["rsrp_dbm"],
                    THRESHOLDS["rsrp_dbm"]["warning"]
                )
            )


        # LOW THROUGHPUT

        if row["throughput_mbps"] < THRESHOLDS["throughput_mbps"]["critical"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "LOW_THROUGHPUT",
                    "CRITICAL",
                    "throughput_mbps",
                    row["throughput_mbps"],
                    THRESHOLDS["throughput_mbps"]["critical"]
                )
            )

        elif row["throughput_mbps"] < THRESHOLDS["throughput_mbps"]["warning"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "LOW_THROUGHPUT",
                    "WARNING",
                    "throughput_mbps",
                    row["throughput_mbps"],
                    THRESHOLDS["throughput_mbps"]["warning"]
                )
            )


        # HIGH PRB

        if row["prb_utilization_pct"] > THRESHOLDS["prb_utilization_pct"]["critical"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_PRB_UTILIZATION",
                    "CRITICAL",
                    "prb_utilization_pct",
                    row["prb_utilization_pct"],
                    THRESHOLDS["prb_utilization_pct"]["critical"]
                )
            )

        elif row["prb_utilization_pct"] > THRESHOLDS["prb_utilization_pct"]["warning"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_PRB_UTILIZATION",
                    "WARNING",
                    "prb_utilization_pct",
                    row["prb_utilization_pct"],
                    THRESHOLDS["prb_utilization_pct"]["warning"]
                )
            )


        # HIGH CPU

        if row["cpu_utilization_pct"] > THRESHOLDS["cpu_utilization_pct"]["critical"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_CPU_UTILIZATION",
                    "CRITICAL",
                    "cpu_utilization_pct",
                    row["cpu_utilization_pct"],
                    THRESHOLDS["cpu_utilization_pct"]["critical"]
                )
            )

        elif row["cpu_utilization_pct"] > THRESHOLDS["cpu_utilization_pct"]["warning"]:

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "HIGH_CPU_UTILIZATION",
                    "WARNING",
                    "cpu_utilization_pct",
                    row["cpu_utilization_pct"],
                    THRESHOLDS["cpu_utilization_pct"]["warning"]
                )
            )


        # CELL OUTAGE

        if (
            row["throughput_mbps"] < 10
            and row["connected_users"] < 15
            and row["rsrp_dbm"] < -115
        ):

            anomalies.append(
                create_anomaly(
                    tower_id,
                    "CELL_OUTAGE",
                    "CRITICAL",
                    "throughput_mbps",
                    row["throughput_mbps"],
                    10
                )
            )


    return anomalies


# ============================================================
# RCA MAP
# ============================================================

RCA_MAP = {

    "HIGH_LATENCY":
        "NETWORK_CONGESTION",

    "HIGH_PACKET_LOSS":
        "NETWORK_DEGRADATION",

    "LOW_SINR":
        "RADIO_INTERFERENCE",

    "LOW_RSRP":
        "RADIO_DEGRADATION",

    "LOW_THROUGHPUT":
        "RADIO_DEGRADATION",

    "HIGH_PRB_UTILIZATION":
        "RESOURCE_CONGESTION",

    "HIGH_CPU_UTILIZATION":
        "PROCESSING_OVERLOAD",

    "CELL_OUTAGE":
        "CELL_FAILURE"
}


# ============================================================
# DETERMINE ROOT CAUSE
# ============================================================

def determine_root_cause(
    anomaly,
    tower_row
):

    anomaly_type = anomaly["anomaly_type"]

    tower_id = anomaly["tower_id"]


    # CELL OUTAGE

    if anomaly_type == "CELL_OUTAGE":

        return {

            "tower_id": tower_id,

            "root_cause": "CELL_FAILURE",

            "confidence": 0.98,

            "evidence": [
                "ANOMALY_DETECTOR",
                "TELELOGS"
            ]
        }


    # POWER ISSUE

    if (
        tower_row["throughput_mbps"] < 30
        and tower_row["cpu_utilization_pct"] < 30
        and tower_row["rsrp_dbm"] < -110
    ):

        return {

            "tower_id": tower_id,

            "root_cause": "POWER_ISSUE",

            "confidence": 0.95,

            "evidence": [
                "ANOMALY_DETECTOR",
                "TELELOGS"
            ]
        }


    # RADIO INTERFERENCE

    if (
        tower_row["sinr_db"] < 5
        and tower_row["packet_loss_pct"] > 2
    ):

        return {

            "tower_id": tower_id,

            "root_cause": "RADIO_INTERFERENCE",

            "confidence": 0.93,

            "evidence": [
                "ANOMALY_DETECTOR",
                "TELELOGS"
            ]
        }


    # RESOURCE CONGESTION

    if (
        tower_row["prb_utilization_pct"] > 80
        and (
            tower_row["latency_ms"] > 50
            or tower_row["throughput_mbps"] < 50
        )
    ):

        return {

            "tower_id": tower_id,

            "root_cause": "RESOURCE_CONGESTION",

            "confidence": 0.95,

            "evidence": [
                "ANOMALY_DETECTOR",
                "TELELOGS"
            ]
        }


    # PROCESSING OVERLOAD

    if tower_row["cpu_utilization_pct"] > 85:

        return {

            "tower_id": tower_id,

            "root_cause": "PROCESSING_OVERLOAD",

            "confidence": 0.94,

            "evidence": [
                "ANOMALY_DETECTOR",
                "TELELOGS"
            ]
        }


    # BACKHAUL FAILURE

    if (
        tower_row["latency_ms"] > 50
        and tower_row["packet_loss_pct"] > 2
        and tower_row["prb_utilization_pct"] < 80
    ):

        return {

            "tower_id": tower_id,

            "root_cause": "BACKHAUL_FAILURE",

            "confidence": 0.90,

            "evidence": [
                "ANOMALY_DETECTOR",
                "TELELOGS"
            ]
        }


    # FALLBACK RCA

    root_cause = RCA_MAP.get(
        anomaly_type,
        "UNKNOWN"
    )

    return {

        "tower_id": tower_id,

        "root_cause": root_cause,

        "confidence": 0.75,

        "evidence": [
            "ANOMALY_DETECTOR",
            "TELELOGS"
        ]
    }


# ============================================================
# OPTIMIZATION MAP
# ============================================================

OPTIMIZATION_MAP = {

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


# ============================================================
# ACTION DESCRIPTIONS
# ============================================================

ACTION_DESCRIPTIONS = {

    "LOAD_BALANCING":
        "Shift traffic toward neighboring cells to reduce overload.",

    "TRAFFIC_OPTIMIZATION":
        "Optimize traffic distribution and scheduling.",

    "RESOURCE_ALLOCATION":
        "Allocate additional radio/network resources.",

    "POWER_CONTROL":
        "Adjust transmit power to improve radio quality and control interference.",

    "ANTENNA_OPTIMIZATION":
        "Review antenna tilt, orientation and configuration.",

    "COVERAGE_OPTIMIZATION":
        "Optimize coverage and neighboring-cell configuration."
}


# ============================================================
# GENERATE OPTIMIZATION
# ============================================================

def generate_optimization(rca_results):

    optimization = []

    for rca in rca_results:

        root_cause = rca["root_cause"]

        actions = OPTIMIZATION_MAP.get(
            root_cause,
            OPTIMIZATION_MAP["UNKNOWN"]
        )

        for action in actions:

            optimization.append({

                "tower_id":
                    rca["tower_id"],

                "root_cause":
                    root_cause,

                "action":
                    action,

                "description":
                    ACTION_DESCRIPTIONS.get(
                        action,
                        ""
                    )
            })

    return optimization


# ============================================================
# BUILD RAG QUERY
# ============================================================

def build_rag_query(
    tower_id,
    anomaly,
    rca
):

    return (
        f"Telecom RAN issue at {tower_id}. "
        f"Detected anomaly: {anomaly['anomaly_type']}. "
        f"Root cause: {rca['root_cause']}. "
        f"Explain the technical cause, relevant "
        f"telecom concepts and recommended "
        f"optimization actions."
    )


# ============================================================
# RESPONSE GENERATOR
# ============================================================

@st.cache_resource
def get_response_generator():

    if not RAG_AVAILABLE:
        return None

    try:

        return ResponseGenerator()

    except Exception:

        return None


# ============================================================
# GENERATE AI RESPONSE
# ============================================================

def generate_ai_response(
    tower_id,
    anomaly,
    rca,
    optimization
):

    generator = get_response_generator()

    if generator is None:

        return (
            "RAG + Qwen is currently unavailable."
        )


    query = build_rag_query(
        tower_id,
        anomaly,
        rca
    )


    try:

        response = generator.generate(
            query
        )

        if isinstance(
            response,
            dict
        ):

            if "answer" in response:

                return response["answer"]

            if "response" in response:

                return response["response"]


        return str(response)


    except Exception as e:

        return (
            f"AI analysis could not be generated: {e}"
        )


# ============================================================
# HEALTH SCORE
# ============================================================

def calculate_health_score(df):

    if df.empty:

        return 0

    score = 100

    critical_count = (
        df["status"] == "Critical"
    ).sum()

    warning_count = (
        df["status"] == "Warning"
    ).sum()

    score -= critical_count * 10

    score -= warning_count * 4

    return max(
        0,
        min(
            100,
            score
        )
    )


# ============================================================
# NETWORK MAP
# ============================================================

def render_network_map(df):

    fig = go.Figure()

    # ========================================================
    # STATUS COLORS
    # ========================================================

    status_colors = {

        "Normal": "#00FF00",

        "Warning": "#FFD700",

        "Critical": "#FF0000"
    }


    # ========================================================
    # DRAW EACH TOWER
    # ========================================================

    for status in [
        "Normal",
        "Warning",
        "Critical"
    ]:

        subset = df[
            df["status"] == status
        ]

        if subset.empty:
            continue

        color = status_colors[status]


        for _, row in subset.iterrows():

            tower_id = row["tower_id"]

            lat, lon = TOWER_LOCATIONS[
                tower_id
            ]


            # =================================================
            # TOWER DIMENSIONS
            # =================================================

            height = 0.0028

            width = 0.0016


            # =================================================
            # TOWER LEFT LEG
            # =================================================

            fig.add_trace(

                go.Scattergeo(

                    lat=[
                        lat - height,
                        lat + height
                    ],

                    lon=[
                        lon - width,
                        lon
                    ],

                    mode="lines",

                    line=dict(
                        color=color,
                        width=6
                    ),

                    hoverinfo="skip",

                    showlegend=False
                )
            )


            # =================================================
            # TOWER RIGHT LEG
            # =================================================

            fig.add_trace(

                go.Scattergeo(

                    lat=[
                        lat - height,
                        lat + height
                    ],

                    lon=[
                        lon + width,
                        lon
                    ],

                    mode="lines",

                    line=dict(
                        color=color,
                        width=6
                    ),

                    hoverinfo="skip",

                    showlegend=False
                )
            )


            # =================================================
            # TOWER CROSS BARS
            # =================================================

            cross_bar_levels = [
                0.00045,
                0.00105,
                0.00165,
                0.00225
            ]


            for level in cross_bar_levels:

                ratio = (
                    level / height
                )

                left_lon = (
                    lon
                    - width * (1 - ratio)
                )

                right_lon = (
                    lon
                    + width * (1 - ratio)
                )

                current_lat = (
                    lat
                    - height
                    + level
                )


                fig.add_trace(

                    go.Scattergeo(

                        lat=[
                            current_lat,
                            current_lat
                        ],

                        lon=[
                            left_lon,
                            right_lon
                        ],

                        mode="lines",

                        line=dict(
                            color=color,
                            width=4
                        ),

                        hoverinfo="skip",

                        showlegend=False
                    )
                )


            # =================================================
            # TOWER TOP ANTENNA
            # =================================================

            fig.add_trace(

                go.Scattergeo(

                    lat=[
                        lat + height,
                        lat + height + 0.0013
                    ],

                    lon=[
                        lon,
                        lon
                    ],

                    mode="lines",

                    line=dict(
                        color=color,
                        width=5
                    ),

                    hoverinfo="skip",

                    showlegend=False
                )
            )


            # =================================================
            # ANTENNA TOP
            # =================================================

            fig.add_trace(

                go.Scattergeo(

                    lat=[
                        lat + height + 0.0013
                    ],

                    lon=[
                        lon
                    ],

                    mode="markers",

                    marker=dict(

                        size=10,

                        color=color,

                        line=dict(
                            color=color,
                            width=2
                        )
                    ),

                    hoverinfo="skip",

                    showlegend=False
                )
            )


            # =================================================
            # TOWER HOVER AREA
            # =================================================

            hover_text = (

                "<b>"
                + tower_id
                + "</b><br>"

                + "Status: "
                + row["status"]
                + "<br>"

                + "Throughput: "
                + f"{row['throughput_mbps']:.1f}"
                + " Mbps<br>"

                + "Latency: "
                + f"{row['latency_ms']:.1f}"
                + " ms<br>"

                + "SINR: "
                + f"{row['sinr_db']:.1f}"
                + " dB<br>"

                + "PRB: "
                + f"{row['prb_utilization_pct']:.1f}"
                + "%"
            )


            fig.add_trace(

                go.Scattergeo(

                    lat=[lat],

                    lon=[lon],

                    mode="markers",

                    marker=dict(

                        size=38,

                        color="rgba(0,0,0,0)"
                    ),

                    hovertext=hover_text,

                    hoverinfo="text",

                    showlegend=False
                )
            )


    # ========================================================
    # LEGEND
    # ========================================================

    for status in [
        "Normal",
        "Warning",
        "Critical"
    ]:

        fig.add_trace(

            go.Scattergeo(

                lat=[None],

                lon=[None],

                mode="markers",

                marker=dict(

                    size=13,

                    color=status_colors[status]
                ),

                name=status
            )
        )


    # ========================================================
    # MAP CONFIGURATION
    # ========================================================

    fig.update_geos(

        center=dict(
            lat=17.39,
            lon=78.50
        ),

        projection_scale=9,

        showland=True,

        showcountries=True,

        showcoastlines=True,

        coastlinecolor="#444444",

        landcolor="#161b22",

        bgcolor="#0e1117"
    )


    # ========================================================
    # MAP LAYOUT
    # ========================================================

    fig.update_layout(

        height=520,

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        paper_bgcolor="#0e1117",

        plot_bgcolor="#0e1117",

        font=dict(
            color="white"
        ),

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=0.01,

            xanchor="center",

            x=0.5
        )
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    st.plotly_chart(

        fig,

        use_container_width=True,

        key="ran_network_map"
    )


# ============================================================
# KPI CHART
# ============================================================

def render_kpi_chart(
    tower_df
):

    if tower_df.empty:
        return


    metrics = [

        "throughput_mbps",

        "latency_ms",

        "sinr_db",

        "prb_utilization_pct",

        "cpu_utilization_pct"
    ]


    values = [

        tower_df.iloc[0][
            metric
        ]

        for metric in metrics
    ]


    labels = [

        "Throughput",

        "Latency",

        "SINR",

        "PRB",

        "CPU"
    ]


    fig = go.Figure(

        go.Bar(

            x=labels,

            y=values,

            text=[
                f"{v:.1f}"
                for v in values
            ],

            textposition="auto"
        )
    )


    fig.update_layout(

        height=350,

        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),

        paper_bgcolor="#0e1117",

        plot_bgcolor="#0e1117",

        font=dict(
            color="white"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-header">'
    '📡 Telecom RAN AI Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">'
    'AI-powered Telecom Radio Access Network monitoring, '
    'anomaly detection, RCA, optimization and RAG-based analysis'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Controls")


    auto_refresh = st.checkbox(
        "Automatic KPI generation",
        value=st.session_state.auto_refresh
    )

    st.session_state.auto_refresh = auto_refresh


    refresh_seconds = st.slider(
        "Generation interval (seconds)",
        min_value=5,
        max_value=30,
        value=st.session_state.refresh_seconds
    )

    st.session_state.refresh_seconds = (
        refresh_seconds
    )


    if st.button(
        "🔄 Generate KPI Cycle",
        use_container_width=True
    ):

        generate_network_cycle()

        st.rerun()


    st.divider()


    st.subheader(
        "📡 Tower Selection"
    )


    selected_tower = st.selectbox(

        "Select Tower",

        TOWER_IDS,

        index=TOWER_IDS.index(
            st.session_state.selected_tower
        )
    )


    st.session_state.selected_tower = (
        selected_tower
    )


    st.divider()


    st.subheader(
        "🔗 Processing Pipeline"
    )


    st.markdown(
        """
        <div class="pipeline-box">
        📡 Live KPI
        <br>↓
        <br>🔍 Anomaly Detection
        <br>↓
        <br>🧠 RCA Engine
        <br>↓
        <br>⚡ Optimization Engine
        <br>↓
        <br>📚 RAG + Qwen
        </div>
        """,
        unsafe_allow_html=True
    )


    if RAG_AVAILABLE:

        st.success(
            "RAG + Qwen available"
        )

    else:

        st.warning(
            "RAG + Qwen unavailable"
        )


# ============================================================
# INITIAL DATA
# ============================================================

if st.session_state.current_kpis.empty:

    generate_network_cycle()


df = st.session_state.current_kpis


# ============================================================
# ANOMALY DETECTION
# ============================================================

anomalies = detect_anomalies(df)

st.session_state.current_anomalies = anomalies


# ============================================================
# RCA
# ============================================================

rca_results = []

for anomaly in anomalies:

    tower_df = df[
        df["tower_id"]
        == anomaly["tower_id"]
    ]

    if tower_df.empty:
        continue

    tower_row = tower_df.iloc[0]

    rca = determine_root_cause(
        anomaly,
        tower_row
    )

    rca_results.append({

        **rca,

        "anomaly_type":
            anomaly["anomaly_type"],

        "severity":
            anomaly["severity"],

        "metric":
            anomaly["metric"],

        "value":
            anomaly["value"],

        "threshold":
            anomaly["threshold"]
    })


st.session_state.current_rca = rca_results


# ============================================================
# OPTIMIZATION
# ============================================================

optimization_results = generate_optimization(
    rca_results
)

st.session_state.current_optimization = (
    optimization_results
)


# ============================================================
# NETWORK SUMMARY
# ============================================================

health_score = calculate_health_score(
    df
)

active_towers = len(df)

normal_count = (
    df["status"] == "Normal"
).sum()

warning_count = (
    df["status"] == "Warning"
).sum()

critical_count = (
    df["status"] == "Critical"
).sum()


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Network Health",
        f"{health_score:.0f}%"
    )


with col2:

    st.metric(
        "Active Towers",
        active_towers
    )


with col3:

    st.metric(
        "Normal",
        normal_count
    )


with col4:

    st.metric(
        "Warning",
        warning_count
    )


with col5:

    st.metric(
        "Critical",
        critical_count
    )


st.divider()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📡 Network Monitoring",
        "🚨 Problems & RCA",
        "🤖 AI Assistant"
    ]
)


# ============================================================
# TAB 1
# NETWORK MONITORING
# ============================================================

with tab1:

    if st.session_state.last_update:

        st.caption(
            "Last KPI generation: "
            + st.session_state.last_update.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " | Cycle: "
            + str(
                st.session_state.simulation_cycle
            )
        )


    # --------------------------------------------------------
    # KPI SUMMARY
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Avg Throughput",
            f"{df['throughput_mbps'].mean():.1f} Mbps"
        )


    with c2:

        st.metric(
            "Avg Latency",
            f"{df['latency_ms'].mean():.1f} ms"
        )


    with c3:

        st.metric(
            "Avg SINR",
            f"{df['sinr_db'].mean():.1f} dB"
        )


    with c4:

        st.metric(
            "Avg PRB",
            f"{df['prb_utilization_pct'].mean():.1f}%"
        )


    st.subheader(
        "📍 RAN Tower Network Map"
    )


    # --------------------------------------------------------
    # NETWORK MAP
    # --------------------------------------------------------

    render_network_map(df)


    st.subheader(
        "📊 Current Tower KPIs"
    )


    display_columns = [

        "tower_id",

        "connected_users",

        "traffic_mbps",

        "throughput_mbps",

        "latency_ms",

        "packet_loss_pct",

        "prb_utilization_pct",

        "sinr_db",

        "rsrp_dbm",

        "cpu_utilization_pct",

        "signal_quality",

        "status"
    ]


    st.dataframe(

        df[
            display_columns
        ],

        use_container_width=True,

        hide_index=True
    )


    st.subheader(
        f"📈 Selected Tower: {selected_tower}"
    )


    selected_df = df[
        df["tower_id"]
        == selected_tower
    ]


    render_kpi_chart(
        selected_df
    )


# ============================================================
# TAB 2
# PROBLEMS + RCA
# ============================================================

with tab2:

    st.subheader(
        "🚨 Detected Anomalies"
    )


    if not anomalies:

        st.success(
            "No anomalies detected in the current cycle."
        )

    else:

        anomaly_df = pd.DataFrame(
            anomalies
        )

        st.dataframe(

            anomaly_df,

            use_container_width=True,

            hide_index=True
        )


    st.divider()


    st.subheader(
        "🧠 Root Cause Analysis"
    )


    if not rca_results:

        st.info(
            "No RCA results available."
        )

    else:

        for rca in rca_results:

            severity = rca["severity"]

            if severity == "CRITICAL":

                st.error(
                    f"🔴 {rca['tower_id']} — "
                    f"{rca['root_cause']}"
                )

            elif severity == "WARNING":

                st.warning(
                    f"🟡 {rca['tower_id']} — "
                    f"{rca['root_cause']}"
                )

            else:

                st.info(
                    f"{rca['tower_id']} — "
                    f"{rca['root_cause']}"
                )


            c1, c2, c3 = st.columns(3)


            with c1:

                st.write(
                    "**Anomaly:**",
                    rca["anomaly_type"]
                )


            with c2:

                st.write(
                    "**Confidence:**",
                    f"{rca['confidence'] * 100:.0f}%"
                )


            with c3:

                st.write(
                    "**Evidence:**",
                    ", ".join(
                        rca["evidence"]
                    )
                )


    st.divider()


    st.subheader(
        "⚡ Optimization Actions"
    )


    if not optimization_results:

        st.info(
            "No optimization actions available."
        )

    else:

        optimization_df = pd.DataFrame(
            optimization_results
        )

        st.dataframe(

            optimization_df,

            use_container_width=True,

            hide_index=True
        )


# ============================================================
# TAB 3
# AI ASSISTANT
# ============================================================

with tab3:

    st.subheader(
        "🤖 RAG + Qwen Telecom AI Assistant"
    )


    if RAG_AVAILABLE:

        st.success(
            "RAG + Qwen pipeline is available."
        )

    else:

        st.warning(
            "RAG + Qwen pipeline is not available."
        )


    # --------------------------------------------------------
    # ACTIVE PROBLEMS
    # --------------------------------------------------------

    if rca_results:

        problem_options = []

        for index, rca in enumerate(
            rca_results
        ):

            problem_options.append(

                f"{index + 1}. "
                f"{rca['tower_id']} - "
                f"{rca['root_cause']}"
            )


        selected_problem = st.selectbox(

            "Select active problem",

            problem_options
        )


        selected_index = (
            problem_options.index(
                selected_problem
            )
        )


        selected_rca = rca_results[
            selected_index
        ]


        tower_id = selected_rca[
            "tower_id"
        ]


        tower_row = df[
            df["tower_id"]
            == tower_id
        ].iloc[0]


        related_anomaly = None


        for anomaly in anomalies:

            if (
                anomaly["tower_id"]
                == tower_id
                and
                anomaly["anomaly_type"]
                ==
                selected_rca["anomaly_type"]
            ):

                related_anomaly = anomaly

                break


        if related_anomaly is None:

            related_anomaly = {

                "anomaly_type":
                    selected_rca["anomaly_type"]
            }


        # ----------------------------------------------------
        # CURRENT PROBLEM
        # ----------------------------------------------------

        st.markdown(
            "### Current Problem"
        )


        st.write(
            f"**Tower:** {tower_id}"
        )

        st.write(
            f"**Anomaly:** "
            f"{selected_rca['anomaly_type']}"
        )

        st.write(
            f"**Root Cause:** "
            f"{selected_rca['root_cause']}"
        )

        st.write(
            f"**Confidence:** "
            f"{selected_rca['confidence'] * 100:.0f}%"
        )


        # ----------------------------------------------------
        # KPI EVIDENCE
        # ----------------------------------------------------

        st.markdown(
            "### KPI Evidence"
        )


        evidence_df = pd.DataFrame({

            "KPI": [

                "Throughput",

                "Latency",

                "Packet Loss",

                "PRB Utilization",

                "SINR",

                "RSRP",

                "CPU Utilization"
            ],

            "Value": [

                f"{tower_row['throughput_mbps']:.2f} Mbps",

                f"{tower_row['latency_ms']:.2f} ms",

                f"{tower_row['packet_loss_pct']:.2f}%",

                f"{tower_row['prb_utilization_pct']:.2f}%",

                f"{tower_row['sinr_db']:.2f} dB",

                f"{tower_row['rsrp_dbm']:.2f} dBm",

                f"{tower_row['cpu_utilization_pct']:.2f}%"
            ]
        })


        st.dataframe(

            evidence_df,

            use_container_width=True,

            hide_index=True
        )


        # ----------------------------------------------------
        # OPTIMIZATION RECOMMENDATION
        # ----------------------------------------------------

        st.markdown(
            "### Optimization Recommendation"
        )


        tower_actions = [

            item

            for item in optimization_results

            if item["tower_id"] == tower_id
        ]


        for action in tower_actions:

            st.write(
                f"• **{action['action']}** — "
                f"{action['description']}"
            )


        # ----------------------------------------------------
        # RAG QUERY
        # ----------------------------------------------------

        rag_query = build_rag_query(

            tower_id,

            related_anomaly,

            selected_rca
        )


        st.markdown(
            "### RAG Query Preview"
        )


        st.code(
            rag_query,
            language="text"
        )


        # ----------------------------------------------------
        # AI ANALYSIS
        # ----------------------------------------------------

        if st.button(
            "🧠 Analyze with RAG + Qwen",
            use_container_width=True
        ):

            with st.spinner(
                "Retrieving telecom knowledge and generating explanation..."
            ):

                answer = generate_ai_response(

                    tower_id,

                    related_anomaly,

                    selected_rca,

                    tower_actions
                )


            st.session_state.last_ai_answer = (
                answer
            )


        if st.session_state.last_ai_answer:

            st.markdown(
                "### AI Analysis"
            )

            st.markdown(
                st.session_state.last_ai_answer
            )


    else:

        st.info(
            "No active network problems are available "
            "for AI analysis in the current cycle."
        )


# ============================================================
# AUTO REFRESH
# ============================================================

if st.session_state.auto_refresh:

    time.sleep(
        st.session_state.refresh_seconds
    )

    generate_network_cycle()

    st.rerun()