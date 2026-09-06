"""
MULTI-SENSOR FUSION FOR INTELLIGENT EQUIPMENT HEALTH MONITORING SYSTEM
Streamlit Community Cloud Deployment Entry Point.
"""
import os
import sys

# Add project root and Equipment_Health_Monitoring to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INNER_DIR = os.path.join(BASE_DIR, "Equipment_Health_Monitoring")

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if INNER_DIR not in sys.path:
    sys.path.insert(0, INNER_DIR)

import pandas as pd
from datetime import datetime
import streamlit as st

from utils.config import load_sensor_thresholds
from database.database import DatabaseManager
from core.sensor_simulator import SensorSimulator
from core.sensor_fusion import SensorFusionEngine
from core.health_engine import EquipmentHealthEngine
from core.anomaly_detector import AnomalyDetector
from core.predictive_maintenance import PredictiveMaintenanceEngine
from utils.helpers import get_status_badge_html, get_status_color

# Page Configuration
st.set_page_config(
    page_title="Multi-Sensor Fusion Equipment Health Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Minimalist Light Custom Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
html, body, .stApp { background-color: #F8FAFC !important; color: #0F172A !important; font-family: 'Inter', sans-serif !important; }
.main .block-container { padding-top: 1rem !important; max-width: 1380px !important; }
#MainMenu, footer, header { visibility: hidden !important; }
.stButton > button { background: linear-gradient(135deg, #4F46E5 0%, #2563EB 100%) !important; color: #FFFFFF !important; font-weight: 800 !important; text-transform: uppercase !important; border: none !important; border-radius: 4px !important; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important; }
.stButton > button:hover { background: linear-gradient(135deg, #4338CA 0%, #1D4ED8 100%) !important; box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3) !important; }
div[data-baseweb="input"] > div { background-color: #FFFFFF !important; border-color: #CBD5E1 !important; color: #0F172A !important; }
div[data-testid="stDataFrame"] { background-color: #FFFFFF !important; border-color: #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

# Instantiate Core Engines
DB = DatabaseManager()
SIMULATOR = SensorSimulator()
FUSION_ENGINE = SensorFusionEngine()
HEALTH_ENGINE = EquipmentHealthEngine()
ANOMALY_DETECTOR = AnomalyDetector(ml_enabled=True)
MAINTENANCE_ENGINE = PredictiveMaintenanceEngine()

# Session State Inputs
if "temp_val" not in st.session_state:
    st.session_state.temp_val = 42.5
    st.session_state.vib_val = 1.8
    st.session_state.press_val = 4.1
    st.session_state.hum_val = 45.0
    st.session_state.curr_val = 12.4
    st.session_state.volt_val = 401.2
    st.session_state.rpm_val = 1480.0

# Header Bar
st.markdown("""
<div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 6px; padding: 14px 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1);">
    <div>
        <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">MULTI-SENSOR FUSION FOR INTELLIGENT EQUIPMENT HEALTH MONITORING</div>
        <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;">Engineering Analysis Application | Asset: M-101 Main Induction Motor [EQ-IND-101]</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3-Column Layout: INPUT -> PROCESS -> OUTPUT
col_input, col_process, col_output = st.columns([1, 1.2, 1.2])

# ==================== SECTION 1: INPUT ====================
with col_input:
    st.markdown("""<div style="font-size: 0.85rem; font-weight: 800; color: #0F172A; text-transform: uppercase; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; margin-bottom: 14px;">1. SENSOR INPUTS</div>""", unsafe_allow_html=True)

    t_val = st.number_input("Temperature (°C)", value=float(st.session_state.temp_val), step=0.5)
    v_val = st.number_input("Vibration (mm/s)", value=float(st.session_state.vib_val), step=0.1)
    p_val = st.number_input("Pressure (bar)", value=float(st.session_state.press_val), step=0.1)
    h_val = st.number_input("Humidity (%)", value=float(st.session_state.hum_val), step=1.0)
    c_val = st.number_input("Current (A)", value=float(st.session_state.curr_val), step=0.2)
    vol_val = st.number_input("Voltage (V)", value=float(st.session_state.volt_val), step=1.0)
    r_val = st.number_input("RPM / Speed (RPM)", value=float(st.session_state.rpm_val), step=10.0)

    inputs_dict = {
        "temperature": t_val,
        "vibration": v_val,
        "pressure": p_val,
        "humidity": h_val,
        "current": c_val,
        "voltage": vol_val,
        "rpm": r_val
    }

    btn_analyze = st.button("ANALYZE EQUIPMENT", use_container_width=True)

    st.markdown("<div style='font-size: 0.72rem; font-weight: 700; color: #64748B; margin-top: 12px; margin-bottom: 6px;'>QUICK PRESETS</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Normal", key="p_norm"):
            base = SIMULATOR._get_baseline_state("normal")
            st.session_state.temp_val, st.session_state.vib_val, st.session_state.press_val, st.session_state.hum_val, st.session_state.curr_val, st.session_state.volt_val, st.session_state.rpm_val = base["temperature"], base["vibration"], base["pressure"], base["humidity"], base["current"], base["voltage"], base["rpm"]
            st.rerun()
    with c2:
        if st.button("Warning", key="p_warn"):
            base = SIMULATOR._get_baseline_state("warning")
            st.session_state.temp_val, st.session_state.vib_val, st.session_state.press_val, st.session_state.hum_val, st.session_state.curr_val, st.session_state.volt_val, st.session_state.rpm_val = base["temperature"], base["vibration"], base["pressure"], base["humidity"], base["current"], base["voltage"], base["rpm"]
            st.rerun()
    with c3:
        if st.button("Critical", key="p_crit"):
            base = SIMULATOR._get_baseline_state("critical")
            st.session_state.temp_val, st.session_state.vib_val, st.session_state.press_val, st.session_state.hum_val, st.session_state.curr_val, st.session_state.volt_val, st.session_state.rpm_val = base["temperature"], base["vibration"], base["pressure"], base["humidity"], base["current"], base["voltage"], base["rpm"]
            st.rerun()

# Execute Core Pipeline
fusion_result = FUSION_ENGINE.process_fusion(inputs_dict)
health_result = HEALTH_ENGINE.evaluate(fusion_result)
anomalies = ANOMALY_DETECTOR.detect_all(fusion_result["cleaned_readings"])
recommendation = MAINTENANCE_ENGINE.evaluate_recommendation(
    health_score=health_result["health_score"],
    health_status=health_result["status"],
    cleaned_readings=fusion_result["cleaned_readings"],
    normalized_risks=fusion_result["normalized_risks"],
    anomalies=anomalies
)

# Extract Main Problem & Affected Sensors
risk_factors = health_result["risk_factors"]
if risk_factors:
    main_problem = risk_factors[0]["reason"]
    affected_sensors = ", ".join([rf["sensor"] for rf in risk_factors])
elif anomalies:
    main_problem = anomalies[0]["description"]
    affected_sensors = anomalies[0].get("sensor", "Multi-Sensor Pattern")
else:
    main_problem = "None (All sensor parameters operating within nominal safe bounds)"
    affected_sensors = "None"

# ==================== SECTION 2: PROCESS ====================
with col_process:
    st.markdown("""<div style="font-size: 0.85rem; font-weight: 800; color: #0F172A; text-transform: uppercase; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; margin-bottom: 14px;">2. MULTI-SENSOR FUSION & ANALYSIS</div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-align: center; margin-bottom: 14px; color: #4F46E5;">
        Sensor Validation ➔ Risk Calculation ➔ Multi-Sensor Fusion ➔ Health Score ➔ Maintenance Analysis
    </div>
    """, unsafe_allow_html=True)

    sensor_config = load_sensor_thresholds()
    table_data = []
    for k, val in fusion_result["cleaned_readings"].items():
        meta = sensor_config.get(k, {})
        name = meta.get("name", k.capitalize())
        unit = meta.get("unit", "")
        r = fusion_result["normalized_risks"].get(k, 0.0)
        w = fusion_result["weights"].get(k, 0.1)
        c = fusion_result["contributions"].get(k, 0.0)
        table_data.append({
            "Sensor": name,
            "Value": f"{val:.1f} {unit}",
            "Risk (0-1)": f"{r:.3f}",
            "Weight": f"{w:.2f}",
            "Contribution": f"{c:.1f}%"
        })

    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

# ==================== SECTION 3: OUTPUT ====================
with col_output:
    st.markdown("""<div style="font-size: 0.85rem; font-weight: 800; color: #0F172A; text-transform: uppercase; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; margin-bottom: 14px;">3. EQUIPMENT HEALTH OUTPUT</div>""", unsafe_allow_html=True)

    score = health_result["health_score"]
    status = health_result["status"]
    color = get_status_color(status)
    badge = get_status_badge_html(status)

    # 1. Health Score
    st.markdown(f"""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px; margin-bottom: 10px;">
        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">1. EQUIPMENT HEALTH SCORE</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 2.8rem; font-weight: 800; color: #0F172A;">{score:.1f} <span style="font-size: 1.1rem; color: #64748B;">/ 100</span></div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Equipment Status
    st.markdown(f"""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px; margin-bottom: 10px;">
        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">2. EQUIPMENT STATUS</div>
        <div style="margin-top: 4px;">{badge}</div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Main Problem
    st.markdown(f"""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px; margin-bottom: 10px;">
        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">3. MAIN PROBLEM DETECTED</div>
        <div style="font-size: 0.9rem; font-weight: 700; color: #2563EB; margin-top: 4px;">{main_problem}</div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Affected Sensors
    st.markdown(f"""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px; margin-bottom: 10px;">
        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">4. AFFECTED SENSORS</div>
        <div style="font-size: 0.9rem; font-weight: 700; color: #0F172A; margin-top: 4px;">{affected_sensors}</div>
    </div>
    """, unsafe_allow_html=True)

    # 5. Maintenance Recommendation
    st.markdown(f"""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid {color}; border-radius: 4px; padding: 12px;">
        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">5. MAINTENANCE RECOMMENDATION</div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #2563EB; margin-top: 4px;">{recommendation.get('recommended_action', 'Routine Inspection')}</div>
        <div style="font-size: 0.82rem; color: #0F172A; margin-top: 4px;">{recommendation.get('reason', '')}</div>
        <div style="font-size: 0.72rem; color: #64748B; margin-top: 6px;">Timeframe: <strong style="color: #0F172A;">{recommendation.get('timeframe', 'Routine')}</strong> | Priority: <strong style="color: {color};">{recommendation.get('priority', 'LOW')}</strong></div>
    </div>
    """, unsafe_allow_html=True)
