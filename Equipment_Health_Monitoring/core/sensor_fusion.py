"""
Multi-Sensor Fusion Engine for Equipment Health Monitoring.

Implements data validation, missing value imputation, sensor normalization,
and weighted multi-sensor risk fusion with extensible strategy design.
"""
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List, Optional

from utils.config import load_sensor_thresholds

class BaseFusionStrategy(ABC):
    """Abstract Strategy interface for multi-sensor fusion algorithms."""
    @abstractmethod
    def fuse(self, normalized_risks: Dict[str, float], weights: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """
        Fuse normalized risk scores into a composite risk score [0, 1]
        and return individual percentage contributions.
        """
        pass

class WeightedRiskFusionStrategy(BaseFusionStrategy):
    """
    Weighted Linear Multi-Sensor Risk Fusion Strategy.
    Composite Risk R = SUM(w_i * r_i) / SUM(w_i)
    Percentage Contribution C_i = (w_i * r_i / R) * 100
    """
    def fuse(self, normalized_risks: Dict[str, float], weights: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        total_weight = sum(weights.get(s, 0.1) for s in normalized_risks)
        if total_weight == 0:
            return 0.0, {s: 0.0 for s in normalized_risks}

        weighted_sum = 0.0
        risk_components = {}

        for sensor, risk in normalized_risks.items():
            w = weights.get(sensor, 0.1)
            comp = w * risk
            risk_components[sensor] = comp
            weighted_sum += comp

        composite_risk = float(weighted_sum / total_weight)
        composite_risk = float(np.clip(composite_risk, 0.0, 1.0))

        # Calculate percentage contributions
        contributions = {}
        if weighted_sum > 1e-6:
            for sensor, comp in risk_components.items():
                contributions[sensor] = round((comp / weighted_sum) * 100.0, 2)
        else:
            # If all risks are near zero, contribution is equal to weight percentage
            for sensor in normalized_risks:
                w = weights.get(sensor, 0.1)
                contributions[sensor] = round((w / total_weight) * 100.0, 2)

        return composite_risk, contributions


class DempsterShaferFusionStrategy(BaseFusionStrategy):
    """
    Placeholder/Advanced Dempster-Shafer Evidence Theory Fusion Strategy.
    Enables future expansion for multi-sensor conflict resolution.
    """
    def fuse(self, normalized_risks: Dict[str, float], weights: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        # High-risk evidence combination
        weighted_fusion = WeightedRiskFusionStrategy()
        return weighted_fusion.fuse(normalized_risks, weights)


class SensorFusionEngine:
    def __init__(self, strategy: Optional[BaseFusionStrategy] = None):
        self.sensor_config = load_sensor_thresholds()
        self.strategy = strategy if strategy is not None else WeightedRiskFusionStrategy()

    def set_strategy(self, strategy: BaseFusionStrategy):
        self.strategy = strategy

    def validate_and_clean_readings(self, readings: Dict[str, Optional[float]]) -> Dict[str, float]:
        """
        Validate sensor values, check physical plausibility, and handle missing values gracefully.
        Imputes missing or out-of-range sensor readings using mid-range safe defaults.
        """
        cleaned = {}
        for sensor_key, meta in self.sensor_config.items():
            val = readings.get(sensor_key)
            min_p = meta.get("min_possible", 0.0)
            max_p = meta.get("max_possible", 1000.0)
            min_s = meta.get("min_safe", 0.0)
            max_s = meta.get("max_safe", 100.0)

            if val is None or not isinstance(val, (int, float)) or np.isnan(val):
                # Impute with mid-safe value
                cleaned[sensor_key] = round((min_s + max_s) / 2.0, 2)
            elif val < min_p or val > max_p:
                # Clip out-of-range corrupt sensor signals
                cleaned[sensor_key] = round(float(np.clip(val, min_p, max_p)), 2)
            else:
                cleaned[sensor_key] = float(val)

        return cleaned

    def normalize_sensor_risk(self, sensor_key: str, val: float) -> float:
        """
        Normalize raw sensor reading into a unified risk index r_i in [0.0, 1.0].
        0.0 = Perfectly Healthy / Nominal
        1.0 = Critical Failure / Out of Bounds
        """
        meta = self.sensor_config.get(sensor_key, {})
        min_safe = meta.get("min_safe", 0.0)
        max_safe = meta.get("max_safe", 100.0)
        warn_high = meta.get("warning_high", max_safe * 1.2)
        crit_high = meta.get("critical_high", warn_high * 1.2)

        warn_low = meta.get("warning_low", None)
        crit_low = meta.get("critical_low", None)

        # Upper bound violation calculation
        if val > max_safe:
            if val >= crit_high:
                return 1.0
            elif val >= warn_high:
                # Scale between warning (0.5) and critical (1.0)
                return 0.5 + 0.5 * ((val - warn_high) / max(crit_high - warn_high, 1e-5))
            else:
                # Scale between safe (0.0) and warning (0.5)
                return 0.5 * ((val - max_safe) / max(warn_high - max_safe, 1e-5))

        # Lower bound violation calculation (e.g. pressure drop, voltage drop)
        if warn_low is not None and val < min_safe:
            if crit_low is not None and val <= crit_low:
                return 1.0
            elif val <= warn_low:
                return 0.5 + 0.5 * ((warn_low - val) / max(warn_low - (crit_low or 0), 1e-5))
            else:
                return 0.5 * ((min_safe - val) / max(min_safe - warn_low, 1e-5))

        # Fully within safe operating window
        return 0.0

    def process_fusion(self, raw_readings: Dict[str, Optional[float]]) -> Dict[str, Any]:
        """
        Complete Multi-Sensor Fusion Pipeline:
        Validation -> Imputation -> Normalization -> Weighted Fusion -> Composite Risk & Contribution
        """
        cleaned_readings = self.validate_and_clean_readings(raw_readings)

        normalized_risks = {}
        weights = {}

        for sensor_key, val in cleaned_readings.items():
            norm_risk = self.normalize_sensor_risk(sensor_key, val)
            normalized_risks[sensor_key] = norm_risk
            weights[sensor_key] = self.sensor_config.get(sensor_key, {}).get("weight", 0.1)

        composite_risk, contributions = self.strategy.fuse(normalized_risks, weights)

        return {
            "cleaned_readings": cleaned_readings,
            "normalized_risks": normalized_risks,
            "weights": weights,
            "composite_risk": composite_risk,
            "contributions": contributions
        }
