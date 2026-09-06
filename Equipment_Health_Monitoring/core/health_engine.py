"""
Equipment Health Engine for calculating explainable Equipment Health Scores (0-100)
and health condition classifications.
"""
from typing import Dict, Any, List

from utils.config import load_sensor_thresholds

class EquipmentHealthEngine:
    def __init__(self):
        self.sensor_config = load_sensor_thresholds()

    def calculate_health_score(self, composite_risk: float) -> float:
        """
        Map composite risk score [0, 1] to Equipment Health Score [0, 100].
        Health Score = (1 - Composite Risk) * 100
        """
        score = (1.0 - composite_risk) * 100.0
        return round(float(max(0.0, min(100.0, score))), 1)

    def classify_status(self, health_score: float) -> str:
        """
        Classify health score into standardized industrial status:
        - 90-100: Healthy
        - 70-89: Normal
        - 40-69: Warning
        - 0-39: Critical
        """
        if health_score >= 90.0:
            return "Healthy"
        elif health_score >= 70.0:
            return "Normal"
        elif health_score >= 40.0:
            return "Warning"
        else:
            return "Critical"

    def generate_explainable_diagnostics(
        self,
        cleaned_readings: Dict[str, float],
        normalized_risks: Dict[str, float],
        contributions: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generate transparent human-readable explanations of equipment condition,
        identifying primary risk factors and normal parameters.
        """
        risk_factors = []
        normal_parameters = []

        for sensor_key, val in cleaned_readings.items():
            meta = self.sensor_config.get(sensor_key, {})
            name = meta.get("name", sensor_key.capitalize())
            unit = meta.get("unit", "")
            risk = normalized_risks.get(sensor_key, 0.0)
            contrib = contributions.get(sensor_key, 0.0)

            max_safe = meta.get("max_safe")
            min_safe = meta.get("min_safe")

            if risk >= 0.5:
                if max_safe is not None and val > max_safe:
                    reason = f"{name} is elevated at {val} {unit} (max safe threshold: {max_safe} {unit}), contributing {contrib}% to total risk."
                elif min_safe is not None and val < min_safe:
                    reason = f"{name} dropped to {val} {unit} (min safe threshold: {min_safe} {unit}), contributing {contrib}% to total risk."
                else:
                    reason = f"{name} at {val} {unit} exhibits high risk index ({round(risk, 2)})."
                risk_factors.append({
                    "sensor": name,
                    "val": f"{val} {unit}",
                    "risk": round(risk, 2),
                    "contribution": f"{contrib}%",
                    "reason": reason
                })
            else:
                normal_parameters.append({
                    "sensor": name,
                    "val": f"{val} {unit}",
                    "status": "Nominal"
                })

        # Sort risk factors by highest risk index
        risk_factors.sort(key=lambda x: x["risk"], reverse=True)

        if not risk_factors:
            summary = "All monitored sensors operate within optimal safety bounds."
        else:
            top = risk_factors[0]
            summary = f"Equipment health degraded primarily due to {top['sensor']} ({top['val']})."

        return {
            "summary": summary,
            "risk_factors": risk_factors,
            "normal_parameters": normal_parameters
        }

    def evaluate(self, fusion_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute full equipment health evaluation given fusion output.
        """
        composite_risk = fusion_output["composite_risk"]
        cleaned_readings = fusion_output["cleaned_readings"]
        normalized_risks = fusion_output["normalized_risks"]
        contributions = fusion_output["contributions"]

        health_score = self.calculate_health_score(composite_risk)
        status = self.classify_status(health_score)
        diagnostics = self.generate_explainable_diagnostics(cleaned_readings, normalized_risks, contributions)

        return {
            "health_score": health_score,
            "status": status,
            "composite_risk": composite_risk,
            "summary": diagnostics["summary"],
            "risk_factors": diagnostics["risk_factors"],
            "normal_parameters": diagnostics["normal_parameters"]
        }
