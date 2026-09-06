"""
Session State Manager for initializing and maintaining application state across pages.
"""
import streamlit as st
import pandas as pd
from datetime import datetime

def init_session_state():
    """Ensure all required session state variables exist with proper defaults."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.active_equipment_id = "EQ-IND-101"
        st.session_state.simulation_profile = "normal"
        st.session_state.auto_refresh = False
        st.session_state.refresh_interval = 5
        st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.simulation_history = []
        st.session_state.ml_anomaly_enabled = True
        st.session_state.active_alerts = []
        st.session_state.current_readings = {}
        st.session_state.current_fusion_result = {}
        st.session_state.current_health_result = {}
        st.session_state.current_anomalies = []
        st.session_state.current_recommendation = {}

def get_active_equipment_id() -> str:
    return st.session_state.get("active_equipment_id", "EQ-IND-101")

def set_active_equipment_id(equipment_id: str):
    st.session_state.active_equipment_id = equipment_id
