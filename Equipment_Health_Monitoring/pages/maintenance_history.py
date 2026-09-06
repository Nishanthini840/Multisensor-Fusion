"""
4. MAINTENANCE & HISTORY PAGE - Combined Action Plan & Historical Analysis.
"""
import streamlit as st
import pandas as pd

from components.charts import create_health_history_chart
from database.database import DatabaseManager

def render():
    """Render Combined Maintenance Recommendations and Historical Analytics."""
    db = DatabaseManager()
    eq_id = st.session_state.active_equipment_id

    st.markdown("""
    <div style="margin-bottom: 10px;">
        <div style="font-size: 1.1rem; font-weight: 800; color: #F8FAFC;">MAINTENANCE PROTOCOL & HISTORY</div>
        <div style="font-size: 0.75rem; color: #64748B;">Actionable maintenance recommendations and historical telemetry logs.</div>
    </div>
    """, unsafe_allow_html=True)

    recommendation = st.session_state.get("current_recommendation", {})
    priority = recommendation.get("priority", "LOW")
    action = recommendation.get("recommended_action", "No immediate maintenance required.")
    reason = recommendation.get("reason", "All parameters operating within safe limits.")
    affected = recommendation.get("affected_sensors", "None")
    timeframe = recommendation.get("timeframe", "Routine cycle")

    if "CRITICAL" in priority.upper():
        color = "#EF4444"
    elif "MEDIUM" in priority.upper() or "WARNING" in priority.upper():
        color = "#F59E0B"
    else:
        color = "#10B981"

    # Current Maintenance Protocol Box
    st.markdown(f"""
    <div style="
        background: #101520;
        border: 1px solid #1C2436;
        border-left: 4px solid {color};
        border-radius: 4px;
        padding: 12px 14px;
        margin-bottom: 14px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">RECOMMENDED MAINTENANCE PROTOCOL</span>
            <span style="background: {color}; color: #FFFFFF; font-weight: 800; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace;">
                PRIORITY: {priority}
            </span>
        </div>

        <div style="font-size: 1.05rem; font-weight: 700; color: #38BDF8; margin-bottom: 4px;">{action}</div>
        <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 8px;"><strong>Diagnostic Reason:</strong> {reason}</div>

        <div style="display: flex; gap: 20px; font-size: 0.75rem; color: #64748B;">
            <div>Affected Sensors: <span style="color: #E2E8F0; font-weight: 600;">{affected}</span></div>
            <div>Timeframe: <span style="color: #E2E8F0; font-weight: 600;">{timeframe}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recent Health Score History Chart
    df_fused = db.get_recent_fused_results(eq_id, limit=30)
    if not df_fused.empty:
        fig_hist = create_health_history_chart(df_fused)
        st.plotly_chart(fig_hist, use_container_width=True)

    # Historical Telemetry Table & CSV Export
    st.markdown("""<div style="font-size: 0.82rem; font-weight: 700; color: #F8FAFC; text-transform: uppercase; margin-bottom: 6px; margin-top: 10px;">RECENT TELEMETRY RECORDS</div>""", unsafe_allow_html=True)
    df_readings = db.get_recent_sensor_readings(eq_id, limit=25)

    if not df_readings.empty:
        c_tbl, c_exp = st.columns([3, 1])
        with c_tbl:
            st.dataframe(df_readings, use_container_width=True, hide_index=True)
        with c_exp:
            csv_bytes = df_readings.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Telemetry CSV",
                data=csv_bytes,
                file_name=f"telemetry_{eq_id}.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    render()
