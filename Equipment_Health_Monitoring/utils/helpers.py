"""
Helper functions for color mapping, status badge generation, and data formatting.
"""
from datetime import datetime

STATUS_COLORS = {
    "Healthy": "#10B981",   # Emerald green
    "Normal": "#3B82F6",    # Electric blue
    "Warning": "#F59E0B",   # Amber orange
    "Critical": "#EF4444",  # Crimson red
    "Unknown": "#6B7280"    # Neutral grey
}

STATUS_BG_COLORS = {
    "Healthy": "rgba(16, 185, 129, 0.15)",
    "Normal": "rgba(59, 130, 246, 0.15)",
    "Warning": "rgba(245, 158, 11, 0.15)",
    "Critical": "rgba(239, 68, 68, 0.15)",
    "Unknown": "rgba(107, 114, 128, 0.15)"
}

STATUS_BORDER_COLORS = {
    "Healthy": "rgba(16, 185, 129, 0.4)",
    "Normal": "rgba(59, 130, 246, 0.4)",
    "Warning": "rgba(245, 158, 11, 0.4)",
    "Critical": "rgba(239, 68, 68, 0.4)",
    "Unknown": "rgba(107, 114, 128, 0.4)"
}

def get_status_color(status: str) -> str:
    """Return hex color string for health/sensor status."""
    return STATUS_COLORS.get(status, "#6B7280")

def get_status_badge_html(status: str) -> str:
    """Generate professional inline HTML pill badge for status."""
    color = STATUS_COLORS.get(status, "#6B7280")
    bg = STATUS_BG_COLORS.get(status, "rgba(107, 114, 128, 0.15)")
    border = STATUS_BORDER_COLORS.get(status, "rgba(107, 114, 128, 0.4)")
    
    return f"""
    <span style="
        background-color: {bg};
        color: {color};
        border: 1px solid {border};
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.82rem;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    ">
        <span style="
            width: 8px;
            height: 8px;
            background-color: {color};
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px {color};
        "></span>
        {status.upper()}
    </span>
    """

def format_timestamp(dt: datetime = None) -> str:
    """Format datetime into standard industrial timestamp string."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_number(val: float, decimals: int = 1) -> str:
    """Format floating point values cleanly."""
    if val is None:
        return "N/A"
    return f"{val:.{decimals}f}"
