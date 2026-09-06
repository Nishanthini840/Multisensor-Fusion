"""
1. OVERVIEW PAGE - Main Landing Dashboard.
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from components.sensor_cards import render_sensor_summary_table
from components.charts import create_health_gauge_chart
from components.status_components import render_alert_banner
from utils.config import load_equipment_config
from utils.helpers import get_status_badge_html, get_status_color

def render():
    """Render Overview Page."""
    eq_id = st.session_state.active_equipment_id
    eq_config = load_equipment_config()
    equipments = {eq["id"]: eq for eq in eq_config.get("equipments", [])}
    eq_info = equipments.get(eq_id, {"name": "M-101 Main Induction Motor", "type": "Induction Motor"})

    health_score = st.session_state.get("current_health_result", {}).get("health_score", 95.0)
    health_status = st.session_state.get("current_health_result", {}).get("status", "Healthy")
    cleaned_readings = st.session_state.get("current_fusion_result", {}).get("cleaned_readings", {})
    normalized_risks = st.session_state.get("current_fusion_result", {}).get("normalized_risks", {})
    active_alerts = st.session_state.get("active_alerts", [])
    recommendation = st.session_state.get("current_recommendation", {})
    last_updated = st.session_state.get("last_updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    badge = get_status_badge_html(health_status)
    status_color = get_status_color(health_status)

    # Top Equipment Header Bar
    st.markdown(f"""
    <div style="
        background: #101520;
        border: 1px solid #1C2436;
        border-radius: 4px;
        padding: 10px 14px;
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <span style="font-weight: 800; font-size: 1.1rem; color: #F8FAFC;">{eq_info['name']}</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #38BDF8; margin-left: 8px;">[{eq_id}]</span>
        </div>
        <div style="font-size: 0.78rem; color: #64748B;">
            STATUS: {badge} | UPDATED: <span style="color: #E2E8F0; font-family: 'JetBrains Mono', monospace;">{last_updated}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Prominent Equipment Health Score Visualization (MAIN FOCUS)
    c_gauge, c_info = st.columns([1, 1])

    with c_gauge:
        st.markdown("""<div style="background: #101520; border: 1px solid #1C2436; border-radius: 4px; padding: 6px;">""", unsafe_allow_html=True)
        fig_gauge = create_health_gauge_chart(health_score, health_status)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

    with c_info:
        # Short Maintenance Recommendation
        rec_action = recommendation.get("recommended_action", "No immediate maintenance required.")
        rec_reason = recommendation.get("reason", "All parameters nominal.")
        rec_priority = recommendation.get("priority", "LOW")

        st.markdown(f"""
        <div style="
            background: #101520;
            border: 1px solid #1C2436;
            border-left: 4px solid {status_color};
            border-radius: 4px;
            padding: 14px;
            height: 100%;
        ">
            <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">MAINTENANCE PROTOCOL SUMMARY</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #38BDF8; margin-top: 4px;">{rec_action}</div>
            <div style="font-size: 0.82rem; color: #CBD5E1; margin-top: 6px;"><strong>Rationale:</strong> {rec_reason}</div>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 8px;">PRIORITY: <span style="color: {status_color}; font-weight: 700;">{rec_priority}</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Active Alert (ONLY IF AN ISSUE EXISTS)
    if active_alerts:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        for alert in active_alerts[:2]:
            render_alert_banner(alert["severity"], alert["title"], alert["message"])

    # Compact Sensor Summary Table below
    st.markdown("""<div style="margin-top: 14px; font-size: 0.85rem; font-weight: 700; color: #F8FAFC; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #1C2436; padding-bottom: 4px; margin-bottom: 8px;">COMPACT SENSOR FEED SUMMARY</div>""", unsafe_allow_html=True)
    if cleaned_readings and normalized_risks:
        render_sensor_summary_table(cleaned_readings, normalized_risks)

if __name__ == "__main__":
    render()
