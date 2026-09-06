"""
3. FUSION & HEALTH ANALYSIS PAGE - Core Multi-Sensor Fusion Innovation.
"""
import streamlit as st
import pandas as pd

from components.charts import create_fusion_contribution_chart
from utils.config import load_sensor_thresholds

def render():
    """Render Multi-Sensor Fusion Engine Analysis."""
    st.markdown("""
    <div style="margin-bottom: 10px;">
        <div style="font-size: 1.1rem; font-weight: 800; color: #F8FAFC;">MULTI-SENSOR FUSION & HEALTH ANALYSIS</div>
        <div style="font-size: 0.75rem; color: #64748B;">Core algorithm combining 7 heterogeneous telemetry channels into a single Equipment Health Index.</div>
    </div>
    """, unsafe_allow_html=True)

    # Core Sequential Process Flow Diagram
    st.markdown("""
    <div style="
        background: #101520;
        border: 1px solid #1C2436;
        border-radius: 4px;
        padding: 10px 14px;
        margin-bottom: 14px;
        text-align: center;
    ">
        <div style="font-size: 0.68rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 6px;">MULTI-SENSOR FUSION SYSTEM FLOW</div>
        <div style="display: flex; justify-content: space-around; align-items: center; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; flex-wrap: wrap; gap: 6px;">
            <span style="color: #38BDF8; font-weight: 700;">Sensor Data</span>
            <span style="color: #475569;">➔</span>
            <span style="color: #FBBF24; font-weight: 700;">Risk Analysis</span>
            <span style="color: #475569;">➔</span>
            <span style="color: #F97316; font-weight: 700;">Weighted Fusion</span>
            <span style="color: #475569;">➔</span>
            <span style="color: #34D399; font-weight: 700;">Health Score</span>
            <span style="color: #475569;">➔</span>
            <span style="color: #10B981; font-weight: 800;">Equipment Status</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cleaned_readings = st.session_state.get("current_fusion_result", {}).get("cleaned_readings", {})
    normalized_risks = st.session_state.get("current_fusion_result", {}).get("normalized_risks", {})
    weights = st.session_state.get("current_fusion_result", {}).get("weights", {})
    contributions = st.session_state.get("current_fusion_result", {}).get("contributions", {})
    composite_risk = st.session_state.get("current_fusion_result", {}).get("composite_risk", 0.05)
    health_score = st.session_state.get("current_health_result", {}).get("health_score", 95.0)
    health_status = st.session_state.get("current_health_result", {}).get("status", "Healthy")

    # Table showing calculated contributions from each sensor
    st.markdown("""<div style="font-size: 0.82rem; font-weight: 700; color: #F8FAFC; text-transform: uppercase; margin-bottom: 6px;">SENSOR RISK & CONTRIBUTION BREAKDOWN</div>""", unsafe_allow_html=True)
    sensor_config = load_sensor_thresholds()
    table_data = []

    for sensor_key, raw_val in cleaned_readings.items():
        meta = sensor_config.get(sensor_key, {})
        name = meta.get("name", sensor_key.capitalize())
        unit = meta.get("unit", "")
        w = weights.get(sensor_key, 0.1)
        r = normalized_risks.get(sensor_key, 0.0)
        c = contributions.get(sensor_key, 0.0)

        table_data.append({
            "Sensor Channel": name,
            "Raw Measurement": f"{raw_val:.1f} {unit}",
            "Risk Index (0-1)": f"{r:.3f}",
            "Weight": f"{w:.2f}",
            "Risk Contribution (%)": f"{c:.1f}%"
        })

    df_matrix = pd.DataFrame(table_data)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)

    # Contribution Chart & Summary Callout
    c_left, c_right = st.columns([1, 1])

    with c_left:
        if contributions:
            fig_donut = create_fusion_contribution_chart(contributions)
            st.plotly_chart(fig_donut, use_container_width=True)

    with c_right:
        st.markdown(f"""
        <div style="
            background: #101520;
            border: 1px solid #1C2436;
            border-radius: 4px;
            padding: 14px;
            margin-top: 10px;
        ">
            <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase;">FUSION RESULT SUMMARY</div>
            <div style="font-size: 1.2rem; font-weight: 800; color: #38BDF8; margin-top: 4px;">Composite Risk Index: <span style="font-family: 'JetBrains Mono', monospace;">{composite_risk:.3f}</span></div>
            <div style="font-size: 1.2rem; font-weight: 800; color: #10B981; margin-top: 2px;">Calculated Health Score: <span style="font-family: 'JetBrains Mono', monospace;">{health_score:.1f} / 100</span></div>
            <div style="font-size: 0.82rem; color: #CBD5E1; margin-top: 8px; line-height: 1.4;">
                The fusion engine validates raw inputs, maps out-of-bounds readings to risk indices, applies domain weights, and fuses them into a single explainable health score.
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
