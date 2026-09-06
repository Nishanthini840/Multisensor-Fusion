"""
Compact Sensor Channel Layout Components.
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.helpers import get_status_badge_html
from utils.config import load_sensor_thresholds

def render_compact_sensor_tile(sensor_key: str, val: float, normalized_risk: float):
    """Render single minimal sensor monitoring tile."""
    sensor_config = load_sensor_thresholds().get(sensor_key, {})
    name = sensor_config.get("name", sensor_key.capitalize())
    unit = sensor_config.get("unit", "")

    if normalized_risk >= 0.8:
        status = "Critical"
        border_color = "#EF4444"
    elif normalized_risk >= 0.4:
        status = "Warning"
        border_color = "#F59E0B"
    elif normalized_risk >= 0.1:
        status = "Normal"
        border_color = "#38BDF8"
    else:
        status = "Healthy"
        border_color = "#10B981"

    badge = get_status_badge_html(status)
    val_display = f"{val:.1f}" if val is not None else "N/A"

    st.markdown(f"""
    <div style="
        background: #101520;
        border: 1px solid #1C2436;
        border-top: 3px solid {border_color};
        border-radius: 4px;
        padding: 8px 12px;
        margin-bottom: 8px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; color: #E2E8F0; font-size: 0.82rem;">{name.upper()}</span>
            {badge}
        </div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #F8FAFC; font-family: 'JetBrains Mono', monospace; margin: 4px 0;">
            {val_display} <span style="font-size: 0.78rem; color: #64748B; font-weight: 400;">{unit}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_compact_sensor_grid(cleaned_readings: Dict[str, float], normalized_risks: Dict[str, float]):
    """Render 7 sensors in a clean 3-column grid."""
    keys = list(cleaned_readings.keys())
    cols = st.columns(3)

    for idx, key in enumerate(keys):
        col = cols[idx % 3]
        with col:
            val = cleaned_readings.get(key)
            risk = normalized_risks.get(key, 0.0)
            render_compact_sensor_tile(key, val, risk)

def render_sensor_summary_table(cleaned_readings: Dict[str, float], normalized_risks: Dict[str, float]):
    """Render compact overview summary table of all sensors."""
    sensor_config = load_sensor_thresholds()
    rows = []

    for key, val in cleaned_readings.items():
        meta = sensor_config.get(key, {})
        name = meta.get("name", key.capitalize())
        unit = meta.get("unit", "")
        risk = normalized_risks.get(key, 0.0)

        if risk >= 0.8:
            cond = "CRITICAL"
        elif risk >= 0.4:
            cond = "WARNING"
        elif risk >= 0.1:
            cond = "NORMAL"
        else:
            cond = "HEALTHY"

        rows.append({
            "Sensor Channel": name,
            "Current Value": f"{val:.1f} {unit}",
            "Status": cond
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
