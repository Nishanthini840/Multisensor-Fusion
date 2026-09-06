"""
Dual-mode Anomaly Detector featuring Rule-Based domain boundary checking
and optional Machine Learning (Isolation Forest) multivariate detection.
"""
import numpy as np
from typing import Dict, Any, List, Optional

from utils.config import load_sensor_thresholds

try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class AnomalyDetector:
    def __init__(self, ml_enabled: bool = True):
        self.sensor_config = load_sensor_thresholds()
        self.ml_enabled = ml_enabled and SKLEARN_AVAILABLE
        self.ml_model: Optional[Any] = None
        self.is_ml_fitted = False
        
        if self.ml_enabled:
            self._init_ml_model()

    def _init_ml_model(self):
        """Initialize and fit Isolation Forest on synthetic nominal baseline data."""
        try:
            self.ml_model = IsolationForest(
                n_estimators=100,
                contamination=0.05,
                random_state=42
            )
            # Create synthetic nominal training matrix (7 channels)
            np.random.seed(42)
            synthetic_train = np.column_stack([
                np.random.normal(43.0, 3.0, 300),   # Temp
                np.random.normal(2.0, 0.5, 300),    # Vibration
                np.random.normal(4.0, 0.3, 300),    # Pressure
                np.random.normal(45.0, 4.0, 300),   # Humidity
                np.random.normal(12.5, 1.0, 300),   # Current
                np.random.normal(400.0, 5.0, 300),  # Voltage
                np.random.normal(1475.0, 15.0, 300) # RPM
            ])
            self.ml_model.fit(synthetic_train)
            self.is_ml_fitted = True
        except Exception as e:
            print(f"ML Model Initialization fallback: {e}")
            self.is_ml_fitted = False

    def detect_rule_based_anomalies(self, readings: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Rule-Based Anomaly Detection against operational boundary limits.
        """
        anomalies = []
        high_risk_sensors = []

        for sensor_key, val in readings.items():
            meta = self.sensor_config.get(sensor_key, {})
            name = meta.get("name", sensor_key.capitalize())
            unit = meta.get("unit", "")
            
            crit_h = meta.get("critical_high")
            warn_h = meta.get("warning_high")
            crit_l = meta.get("critical_low")
            warn_l = meta.get("warning_low")
            max_safe = meta.get("max_safe")
            min_safe = meta.get("min_safe")

            # High bound checks
            if crit_h is not None and val >= crit_h:
                anomalies.append({
                    "type": "Critical Sensor Breach",
                    "severity": "CRITICAL",
                    "sensor": name,
                    "val": f"{val} {unit}",
                    "description": f"Critical limit exceeded: {name} reached {val} {unit} (Threshold: {crit_h} {unit}).",
                    "is_ml": False
                })
                high_risk_sensors.append(name)
            elif warn_h is not None and val >= warn_h:
                anomalies.append({
                    "type": "Warning Threshold Exceeded",
                    "severity": "WARNING",
                    "sensor": name,
                    "val": f"{val} {unit}",
                    "description": f"Warning threshold exceeded: {name} at {val} {unit} (Threshold: {warn_h} {unit}).",
                    "is_ml": False
                })
                high_risk_sensors.append(name)

            # Low bound checks
            if crit_l is not None and val <= crit_l:
                anomalies.append({
                    "type": "Critical Low Sensor Breach",
                    "severity": "CRITICAL",
                    "sensor": name,
                    "val": f"{val} {unit}",
                    "description": f"Critical drop detected: {name} fell to {val} {unit} (Threshold: {crit_l} {unit}).",
                    "is_ml": False
                })
                high_risk_sensors.append(name)
            elif warn_l is not None and val <= warn_l:
                anomalies.append({
                    "type": "Low Warning Level",
                    "severity": "WARNING",
                    "sensor": name,
                    "val": f"{val} {unit}",
                    "description": f"Warning drop detected: {name} at {val} {unit} (Threshold: {warn_l} {unit}).",
                    "is_ml": False
                })
                high_risk_sensors.append(name)

        # Multi-sensor simultaneous risk check
        if len(high_risk_sensors) >= 2:
            anomalies.append({
                "type": "Multi-Sensor Coupled Anomaly",
                "severity": "CRITICAL" if len(high_risk_sensors) >= 3 else "WARNING",
                "sensor": ", ".join(high_risk_sensors),
                "val": "Multiple",
                "description": f"Correlated multi-sensor deviation detected across: {', '.join(high_risk_sensors)}.",
                "is_ml": False
            })

        return anomalies

    def detect_ml_anomalies(self, readings: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Machine Learning Anomaly Detection using Isolation Forest outlier score.
        """
        if not (self.ml_enabled and self.is_ml_fitted and self.ml_model is not None):
            return []

        try:
            # Order vector according to standard channels
            feature_vector = np.array([[
                readings.get("temperature", 43.0),
                readings.get("vibration", 2.0),
                readings.get("pressure", 4.0),
                readings.get("humidity", 45.0),
                readings.get("current", 12.5),
                readings.get("voltage", 400.0),
                readings.get("rpm", 1475.0)
            ]])

            pred = self.ml_model.predict(feature_vector)[0]  # -1 = anomaly, 1 = normal
            score = self.ml_model.decision_function(feature_vector)[0]

            if pred == -1:
                severity = "CRITICAL" if score < -0.15 else "WARNING"
                return [{
                    "type": "ML Multivariate Outlier",
                    "severity": severity,
                    "sensor": "Multi-Sensor Pattern",
                    "val": f"Score: {round(float(score), 3)}",
                    "description": f"Isolation Forest detected non-linear multivariate anomaly (Outlier Score: {round(float(score), 3)}).",
                    "is_ml": True
                }]
        except Exception as e:
            print(f"ML Detection Execution Error: {e}")

        return []

    def detect_all(self, readings: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Run both Rule-Based and ML anomaly detectors and aggregate results.
        """
        rule_anomalies = self.detect_rule_based_anomalies(readings)
        ml_anomalies = self.detect_ml_anomalies(readings) if self.ml_enabled else []
        
        return rule_anomalies + ml_anomalies
