"""
Focused Industrial Visualizations.
"""
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

DARK_PANEL_BG = "#101520"
MONO_FONT = "JetBrains Mono, monospace"
FONT_FAMILY = "Inter, sans-serif"

def create_health_gauge_chart(health_score: float, status: str) -> go.Figure:
    """Create prominent equipment health gauge chart."""
    if health_score >= 90:
        gauge_color = "#10B981"
    elif health_score >= 70:
        gauge_color = "#38BDF8"
    elif health_score >= 40:
        gauge_color = "#F59E0B"
    else:
        gauge_color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        number={"suffix": "/100", "font": {"size": 46, "color": "#F8FAFC", "family": MONO_FONT}},
        title={"text": f"STATUS: {status.upper()}", "font": {"size": 14, "color": gauge_color, "family": MONO_FONT}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#334155", "dtick": 25},
            "bar": {"color": gauge_color, "thickness": 0.3},
            "bgcolor": "#1E293B",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(239, 68, 68, 0.2)"},
                {"range": [40, 70], "color": "rgba(245, 158, 11, 0.2)"},
                {"range": [70, 90], "color": "rgba(56, 189, 248, 0.2)"},
                {"range": [90, 100], "color": "rgba(16, 185, 129, 0.2)"}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#CBD5E1", "family": FONT_FAMILY},
        margin=dict(l=15, r=15, t=25, b=15),
        height=210
    )
    return fig

def create_fusion_contribution_chart(contributions: Dict[str, float]) -> go.Figure:
    """Create simple sensor contribution chart."""
    labels = [k.upper() for k in contributions.keys()]
    values = list(contributions.values())
    colors = ["#EF4444", "#F59E0B", "#38BDF8", "#10B981", "#8B5CF6", "#EC4899", "#06B6D4"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#101520", width=2)),
        textinfo="label+percent",
        textposition="outside"
    )])

    fig.update_layout(
        title={"text": "Sensor Risk Contribution Breakdown", "font": {"size": 13, "color": "#94A3B8", "family": MONO_FONT}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#CBD5E1", "family": FONT_FAMILY, "size": 11},
        showlegend=False,
        margin=dict(l=15, r=15, t=35, b=15),
        height=240
    )
    return fig

def create_health_history_chart(df_fused: pd.DataFrame) -> go.Figure:
    """Create focused line chart of equipment health score history."""
    if df_fused.empty:
        fig = go.Figure()
        fig.update_layout(title="No Health History", paper_bgcolor="rgba(0,0,0,0)")
        return fig

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_fused["timestamp"],
        y=df_fused["health_score"],
        mode="lines+markers",
        line=dict(color="#10B981", width=2.5),
        marker=dict(size=5, color="#34D399"),
        name="Health Score"
    ))

    fig.update_layout(
        title={"text": "Equipment Health Score History", "font": {"size": 13, "color": "#94A3B8", "family": MONO_FONT}},
        xaxis=dict(title="", gridcolor="#1E293B", tickfont=dict(color="#64748B", size=10)),
        yaxis=dict(title="Health Score", range=[0, 105], gridcolor="#1E293B", tickfont=dict(color="#64748B", size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=DARK_PANEL_BG,
        font={"color": "#CBD5E1", "family": FONT_FAMILY},
        margin=dict(l=35, r=15, t=35, b=30),
        height=230
    )
    return fig
