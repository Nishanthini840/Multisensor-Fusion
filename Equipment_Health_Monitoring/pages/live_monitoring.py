"""
2. LIVE MONITORING PAGE - Essential Sensor Feeds & Simulation Console.
"""
import streamlit as st
from components.sensor_cards import render_compact_sensor_grid

def render():
    """Render Live Telemetry Monitoring."""
    st.markdown("""
    <div style="margin-bottom: 10px;">
        <div style="font-size: 1.1rem; font-weight: 800; color: #F8FAFC;">LIVE EQUIPMENT MONITORING</div>
        <div style="font-size: 0.75rem; color: #64748B;">Real-time 7-channel telemetry feed and condition status.</div>
    </div>
    """, unsafe_allow_html=True)

    # Necessary Simulation Controls Only
    st.markdown("""
    <div style="background: #101520; border: 1px solid #1C2436; border-radius: 4px; padding: 8px; margin-bottom: 12px;">
        <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 6px;">SIMULATION CONTROLS</div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Normal Condition", use_container_width=True):
            st.session_state.simulation_profile = "normal"
            st.rerun()
    with c2:
        if st.button("Warning Condition", use_container_width=True):
            st.session_state.simulation_profile = "warning"
            st.rerun()
    with c3:
        if st.button("Critical Condition", use_container_width=True):
            st.session_state.simulation_profile = "critical"
            st.rerun()
    with c4:
        if st.button("Reset", use_container_width=True):
            st.session_state.simulation_profile = "normal"
            st.rerun()
    st.markdown("""</div>""", unsafe_allow_html=True)

    # Essential 7-Sensor Telemetry Grid
    cleaned_readings = st.session_state.get("current_fusion_result", {}).get("cleaned_readings", {})
    normalized_risks = st.session_state.get("current_fusion_result", {}).get("normalized_risks", {})

    if cleaned_readings and normalized_risks:
        render_compact_sensor_grid(cleaned_readings, normalized_risks)

if __name__ == "__main__":
    render()
