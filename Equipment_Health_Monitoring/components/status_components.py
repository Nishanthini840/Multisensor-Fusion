"""
Industrial Status Banners, Technical Section Headers, and Action Cards.
"""
import streamlit as st
from typing import Dict, Any

def render_section_header(title: str, subtitle: str = ""):
    """Render a clean technical section header."""
    st.markdown(f"""
    <div style="margin-top: 14px; margin-bottom: 10px; border-bottom: 1px solid #1B2234; padding-bottom: 4px;">
        <div style="font-size: 0.85rem; font-weight: 800; color: #F8FAFC; text-transform: uppercase; letter-spacing: 0.8px;">{title}</div>
        {f'<div style="font-size: 0.75rem; color: #64748B; margin-top: 2px;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_alert_banner(severity: str, title: str, message: str):
    """Render a compact industrial alert banner."""
    if severity.upper() == "CRITICAL":
        border_color = "#EF4444"
        bg_color = "rgba(239, 68, 68, 0.1)"
    elif severity.upper() == "WARNING":
        border_color = "#F59E0B"
        bg_color = "rgba(245, 158, 11, 0.1)"
    else:
        border_color = "#38BDF8"
        bg_color = "rgba(56, 189, 248, 0.1)"

    st.markdown(f"""
    <div style="
        background: {bg_color};
        border-left: 3px solid {border_color};
        border-radius: 4px;
        padding: 8px 12px;
        margin-bottom: 8px;
    ">
        <div style="font-weight: 700; color: #F8FAFC; font-size: 0.82rem; letter-spacing: 0.3px;">
            [{severity.upper()}] {title}
        </div>
        <div style="font-size: 0.78rem; color: #CBD5E1; margin-top: 2px;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_recommendation_card(recommendation: Dict[str, Any]):
    """Render structured predictive maintenance recommendation card."""
    if not recommendation:
        st.info("No active maintenance protocol prescribed.")
        return

    priority = recommendation.get("priority", "LOW")
    action = recommendation.get("recommended_action", "Routine Inspection")
    reason = recommendation.get("reason", "All parameters nominal.")
    affected = recommendation.get("affected_sensors", "None")
    timeframe = recommendation.get("timeframe", "Routine cycle")

    if "CRITICAL" in priority.upper():
        color = "#EF4444"
    elif "MEDIUM" in priority.upper() or "WARNING" in priority.upper():
        color = "#F59E0B"
    else:
        color = "#10B981"

    st.markdown(f"""
    <div style="
        background: #0E131F;
        border: 1px solid #1B2234;
        border-left: 4px solid {color};
        border-radius: 4px;
        padding: 14px 16px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; font-size: 0.82rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">Recommended Action Protocol</span>
            <span style="
                background: {color};
                color: #FFFFFF;
                font-weight: 800;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.7rem;
                font-family: 'JetBrains Mono', monospace;
            ">PRIORITY: {priority}</span>
        </div>

        <div style="font-size: 1.05rem; font-weight: 700; color: #38BDF8; margin-bottom: 6px;">
            {action}
        </div>

        <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.4; margin-bottom: 10px; background: #0A0D12; padding: 8px 10px; border-radius: 4px; border: 1px solid #192030;">
            <strong>Diagnostic Rationale:</strong> {reason}
        </div>

        <div style="display: flex; gap: 20px; font-size: 0.75rem; color: #64748B;">
            <div>Affected Channels: <span style="color: #E2E8F0; font-weight: 600;">{affected}</span></div>
            <div>Timeframe: <span style="color: #E2E8F0; font-weight: 600;">{timeframe}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
