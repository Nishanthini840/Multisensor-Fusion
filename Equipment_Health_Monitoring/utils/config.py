"""
Configuration loader utility for sensor thresholds and equipment specifications.
"""
import os
import json
from typing import Dict, Any

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def get_data_filepath(filename: str) -> str:
    return os.path.join(DEFAULT_DATA_DIR, filename)

def load_sensor_thresholds() -> Dict[str, Any]:
    """Load sensor operational boundaries and weights from JSON configuration."""
    filepath = get_data_filepath("sensor_thresholds.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("sensors", {})
        except Exception as e:
            print(f"Error loading sensor_thresholds.json: {e}")
    
    # Fallback default configuration
    return {
        "temperature": {"name": "Temperature", "unit": "°C", "weight": 0.20, "min_safe": 20.0, "max_safe": 65.0, "warning_high": 75.0, "critical_high": 90.0, "min_possible": 0.0, "max_possible": 120.0},
        "vibration": {"name": "Vibration", "unit": "mm/s", "weight": 0.25, "min_safe": 0.0, "max_safe": 4.5, "warning_high": 7.5, "critical_high": 12.0, "min_possible": 0.0, "max_possible": 25.0},
        "pressure": {"name": "Pressure", "unit": "bar", "weight": 0.15, "min_safe": 2.5, "max_safe": 5.5, "warning_low": 2.0, "warning_high": 6.5, "critical_low": 1.2, "critical_high": 8.0, "min_possible": 0.0, "max_possible": 15.0},
        "humidity": {"name": "Humidity", "unit": "%", "weight": 0.05, "min_safe": 30.0, "max_safe": 65.0, "warning_low": 20.0, "warning_high": 75.0, "critical_low": 10.0, "critical_high": 90.0, "min_possible": 0.0, "max_possible": 100.0},
        "current": {"name": "Current", "unit": "A", "weight": 0.15, "min_safe": 5.0, "max_safe": 18.0, "warning_high": 22.0, "critical_high": 28.0, "min_possible": 0.0, "max_possible": 50.0},
        "voltage": {"name": "Voltage", "unit": "V", "weight": 0.10, "min_safe": 380.0, "max_safe": 420.0, "warning_low": 360.0, "warning_high": 435.0, "critical_low": 340.0, "critical_high": 460.0, "min_possible": 0.0, "max_possible": 500.0},
        "rpm": {"name": "RPM / Speed", "unit": "RPM", "weight": 0.10, "min_safe": 1400.0, "max_safe": 1780.0, "warning_low": 1250.0, "warning_high": 1850.0, "critical_low": 1000.0, "critical_high": 2000.0, "min_possible": 0.0, "max_possible": 3000.0}
    }

def load_equipment_config() -> Dict[str, Any]:
    """Load equipment registry and active equipment selection."""
    filepath = get_data_filepath("equipment_config.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading equipment_config.json: {e}")
            
    return {
        "equipments": [
            {"id": "EQ-IND-101", "name": "M-101 Main Induction Motor", "type": "Induction Motor", "location": "Production Bay Alpha", "installation_date": "2022-03-15", "rated_power": "45 kW", "manufacturer": "Siemens Industrial", "status": "Active"}
        ],
        "active_equipment_id": "EQ-IND-101"
    }
