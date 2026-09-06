"""
Compact Industrial KPI Metric Cards.
"""
import streamlit as st
from utils.helpers import get_status_color, get_status_badge_html

def render_essential_kpis(status: str, composite_risk: float, active_alerts_count: int, priority: str):
    """Render 4 essential control panel indicators next to the health gauge."""
    color = get_status_color(status)
    badge_html = get_status_badge_html(status)

    if "CRITICAL" in priority.upper():
        p_color = "#EF4444"
    elif "MEDIUM" in priority.upper() or "WARNING" in priority.upper():
        p_color = "#F59E0B"
    else:
        p_color = "#10B981"

    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; height: 100%;">
        <div style="
            background: #0E131F;
            border: 1px solid #1B2234;
            border-left: 3px solid {color};
            border-radius: 4px;
            padding: 10px 14px;
        ">
            <div style="font-size: 0.7rem; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Current Status</div>
            <div style="margin-top: 4px;">{badge_html}</div>
        </div>

        <div style="
            background: #0E131F;
            border: 1px solid #1B2234;
            border-left: 3px solid #38BDF8;
            border-radius: 4px;
            padding: 10px 14px;
        ">
            <div style="font-size: 0.7rem; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Composite Risk</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #38BDF8; font-family: 'JetBrains Mono', monospace;">{composite_risk:.3f}</div>
        </div>

        <div style="
            background: #0E131F;
            border: 1px solid #1B2234;
            border-left: 3px solid {'#EF4444' if active_alerts_count > 0 else '#10B981'};
            border-radius: 4px;
            padding: 10px 14px;
        ">
            <div style="font-size: 0.7rem; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Active Alerts</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: {'#EF4444' if active_alerts_count > 0 else '#10B981'}; font-family: 'JetBrains Mono', monospace;">{active_alerts_count}</div>
        </div>

        <div style="
            background: #0E131F;
            border: 1px solid #1B2234;
            border-left: 3px solid {p_color};
            border-radius: 4px;
            padding: 10px 14px;
        ">
            <div style="font-size: 0.7rem; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Maintenance Priority</div>
            <div style="font-size: 1.05rem; font-weight: 800; color: {p_color}; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">{priority}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
