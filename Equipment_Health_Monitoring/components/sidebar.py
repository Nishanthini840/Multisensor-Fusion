"""
Minimal Industrial Sidebar Control Panel.
"""
import streamlit as st
from utils.config import load_equipment_config

def render_sidebar():
    """Render minimal equipment selector and simulation controls."""
    st.sidebar.markdown("""
        <div style="padding: 4px 0 10px 0; border-bottom: 1px solid #1C2436; margin-bottom: 10px;">
            <div style="font-weight: 800; font-size: 1rem; color: #F8FAFC; letter-spacing: 0.5px;">EQUIPMENT MONITOR</div>
            <div style="font-size: 0.68rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">Multi-Sensor Fusion Engine</div>
        </div>
    """, unsafe_allow_html=True)

    # Equipment Asset Selector
    eq_config = load_equipment_config()
    equipments = eq_config.get("equipments", [])
    eq_options = {eq["id"]: f"{eq['name']} ({eq['id']})" for eq in equipments}

    selected_id = st.sidebar.selectbox(
        "EQUIPMENT",
        options=list(eq_options.keys()),
        format_func=lambda x: eq_options[x],
        index=0
    )
    st.session_state.active_equipment_id = selected_id

    st.sidebar.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("""<div style='font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>SIMULATION CONTROLS</div>""", unsafe_allow_html=True)

    c1, c2 = st.sidebar.columns(2)
    with c1:
        if st.button("Normal", use_container_width=True):
            st.session_state.simulation_profile = "normal"
            st.rerun()
    with c2:
        if st.button("Warning", use_container_width=True):
            st.session_state.simulation_profile = "warning"
            st.rerun()

    c3, c4 = st.sidebar.columns(2)
    with c3:
        if st.button("Critical", use_container_width=True):
            st.session_state.simulation_profile = "critical"
            st.rerun()
    with c4:
        if st.button("Reset", use_container_width=True):
            st.session_state.simulation_profile = "normal"
            st.rerun()

    st.sidebar.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.session_state.ml_anomaly_enabled = st.sidebar.checkbox(
        "ML Isolation Forest",
        value=st.session_state.get("ml_anomaly_enabled", True)
    )
