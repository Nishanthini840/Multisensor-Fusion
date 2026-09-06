"""
Realistic physics-aware Multi-Sensor Simulator for industrial machinery monitoring.
"""
import random
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional

from utils.config import load_sensor_thresholds

class SensorSimulator:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.thresholds = load_sensor_thresholds()
        self.current_state = self._get_baseline_state("normal")

    def _get_baseline_state(self, profile: str) -> Dict[str, float]:
        """Generate baseline physical parameters based on requested profile."""
        if profile == "normal":
            return {
                "temperature": random.uniform(38.0, 48.0),
                "vibration": random.uniform(1.2, 2.5),
                "pressure": random.uniform(3.8, 4.5),
                "humidity": random.uniform(40.0, 52.0),
                "current": random.uniform(11.0, 14.5),
                "voltage": random.uniform(395.0, 405.0),
                "rpm": random.uniform(1460.0, 1490.0)
            }
        elif profile == "warning":
            return {
                "temperature": random.uniform(66.0, 74.0),
                "vibration": random.uniform(5.5, 7.2),
                "pressure": random.uniform(2.1, 2.4),
                "humidity": random.uniform(22.0, 28.0),
                "current": random.uniform(19.0, 21.8),
                "voltage": random.uniform(365.0, 375.0),
                "rpm": random.uniform(1280.0, 1340.0)
            }
        elif profile == "critical":
            return {
                "temperature": random.uniform(86.0, 98.0),
                "vibration": random.uniform(10.5, 15.2),
                "pressure": random.uniform(1.2, 1.7),
                "humidity": random.uniform(12.0, 18.0),
                "current": random.uniform(25.5, 31.0),
                "voltage": random.uniform(342.0, 355.0),
                "rpm": random.uniform(1050.0, 1220.0)
            }
        elif profile == "fault_temp":
            state = self._get_baseline_state("normal")
            state["temperature"] = random.uniform(92.0, 110.0)
            return state
        elif profile == "fault_vibration":
            state = self._get_baseline_state("normal")
            state["vibration"] = random.uniform(14.0, 19.5)
            return state
        elif profile == "fault_pressure":
            state = self._get_baseline_state("normal")
            state["pressure"] = random.uniform(0.5, 1.1)
            return state
        elif profile == "fault_current":
            state = self._get_baseline_state("normal")
            state["current"] = random.uniform(32.0, 40.0)
            state["temperature"] += 15.0
            return state
        else:
            return self._get_baseline_state("normal")

    def step(self, profile: str = "normal", drift: bool = True) -> Dict[str, float]:
        """Advance time by one step, applying realistic noise and drift."""
        base = self._get_baseline_state(profile)
        
        # Apply smooth random walk or jitter
        readings = {}
        for key in base:
            if drift:
                noise = np.random.normal(0, 0.02 * base[key])
                val = base[key] + noise
            else:
                val = base[key]
                
            # Ensure within physical boundaries
            meta = self.thresholds.get(key, {})
            min_p = meta.get("min_possible", 0.0)
            max_p = meta.get("max_possible", 1000.0)
            readings[key] = round(float(np.clip(val, min_p, max_p)), 2)

        self.current_state = readings
        return readings

    def inject_sensor_fault(self, sensor_key: str, fault_type: str = "high") -> Dict[str, float]:
        """Inject a specific fault into a chosen sensor channel."""
        readings = self.step(profile="normal")
        meta = self.thresholds.get(sensor_key, {})
        
        if fault_type == "high":
            readings[sensor_key] = round(meta.get("critical_high", meta.get("max_safe", 50.0) * 1.5) * 1.1, 2)
        elif fault_type == "low":
            readings[sensor_key] = round(meta.get("critical_low", meta.get("min_safe", 10.0) * 0.5) * 0.8, 2)
        elif fault_type == "missing":
            readings[sensor_key] = None
        elif fault_type == "spike":
            readings[sensor_key] = round(meta.get("max_possible", 100.0) * 0.95, 2)
            
        return readings
