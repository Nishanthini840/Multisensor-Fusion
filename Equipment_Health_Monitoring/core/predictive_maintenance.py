"""
Predictive Maintenance Engine mapping multi-sensor fusion states
and detected anomalies to actionable industrial maintenance recommendations.
"""
from typing import Dict, Any, List

class PredictiveMaintenanceEngine:
    def evaluate_recommendation(
        self,
        health_score: float,
        health_status: str,
        cleaned_readings: Dict[str, float],
        normalized_risks: Dict[str, float],
        anomalies: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate contextual predictive maintenance protocol with priority,
        recommended action, diagnostic reason, affected sensors, and timeframe.
        """
        vibration_risk = normalized_risks.get("vibration", 0.0)
        temp_risk = normalized_risks.get("temperature", 0.0)
        current_risk = normalized_risks.get("current", 0.0)
        pressure_risk = normalized_risks.get("pressure", 0.0)
        voltage_risk = normalized_risks.get("voltage", 0.0)
        rpm_risk = normalized_risks.get("rpm", 0.0)

        temp = cleaned_readings.get("temperature", 45.0)
        vib = cleaned_readings.get("vibration", 2.0)
        curr = cleaned_readings.get("current", 12.0)
        press = cleaned_readings.get("pressure", 4.0)
        volt = cleaned_readings.get("voltage", 400.0)
        rpm = cleaned_readings.get("rpm", 1475.0)

        affected = []
        for s, r in normalized_risks.items():
            if r >= 0.4:
                affected.append(s.capitalize())

        affected_str = ", ".join(affected) if affected else "None"

        # Diagnostic failure mode evaluation
        if health_status == "Critical":
            if vibration_risk >= 0.5 and temp_risk >= 0.5:
                return {
                    "priority": "HIGH / CRITICAL",
                    "recommended_action": "Emergency Shutdown & Mechanical Bearing Replacement",
                    "reason": f"Severe bearing degradation detected. High vibration ({vib} mm/s) coupled with thermal elevation ({temp} °C) indicates impending bearing seizure.",
                    "affected_sensors": affected_str,
                    "risk_level": "Critical",
                    "timeframe": "Immediate (within 2 hours)"
                }
            elif current_risk >= 0.5 and (voltage_risk >= 0.4 or temp_risk >= 0.4):
                return {
                    "priority": "HIGH / CRITICAL",
                    "recommended_action": "Inspect Motor Stator Windings & Power Supply Inverter",
                    "reason": f"Electrical overload risk. Excessive phase current draw ({curr} A) with voltage instability ({volt} V) suggests winding shorting or power phase unbalance.",
                    "affected_sensors": affected_str,
                    "risk_level": "Critical",
                    "timeframe": "Immediate (within 4 hours)"
                }
            elif pressure_risk >= 0.5:
                return {
                    "priority": "HIGH / CRITICAL",
                    "recommended_action": "Inspect Hydraulic/Pneumatic Lines & Pressure Relief Valves",
                    "reason": f"Critical pressure boundary breach ({press} bar). Risk of fluid leakage, cavitation, or pipe rupture.",
                    "affected_sensors": affected_str,
                    "risk_level": "Critical",
                    "timeframe": "Within 6 hours"
                }
            else:
                return {
                    "priority": "HIGH / CRITICAL",
                    "recommended_action": "Comprehensive Multi-System Equipment Overhaul",
                    "reason": f"Multiple sensors indicate critical operational degradation (Health Score: {health_score}/100).",
                    "affected_sensors": affected_str,
                    "risk_level": "Critical",
                    "timeframe": "Within 12 hours"
                }

        elif health_status == "Warning":
            if vibration_risk >= 0.4:
                return {
                    "priority": "MEDIUM",
                    "recommended_action": "Perform Shaft Alignment & Dynamic Balancing Test",
                    "reason": f"Vibration level ({vib} mm/s) exceeds normal ISO limits. Check mounting bolt torque and rotor balance.",
                    "affected_sensors": affected_str,
                    "risk_level": "Warning",
                    "timeframe": "Within 24–48 hours"
                }
            elif temp_risk >= 0.4:
                return {
                    "priority": "MEDIUM",
                    "recommended_action": "Inspect Cooling System & Bearing Lubrication",
                    "reason": f"Operating temperature elevated ({temp} °C). Verify oil level, coolant flow, and clean ventilation fins.",
                    "affected_sensors": affected_str,
                    "risk_level": "Warning",
                    "timeframe": "Within 48 hours"
                }
            elif current_risk >= 0.4:
                return {
                    "priority": "MEDIUM",
                    "recommended_action": "Check Electrical Load & Driven Mechanical Coupling",
                    "reason": f"Motor current draw ({curr} A) above normal rating. Verify mechanical load is not binding.",
                    "affected_sensors": affected_str,
                    "risk_level": "Warning",
                    "timeframe": "Within 3 days"
                }
            else:
                return {
                    "priority": "MEDIUM",
                    "recommended_action": "Schedule Diagnostic Field Inspection",
                    "reason": f"Sensor fusion indicates mild degradation trend (Health Score: {health_score}/100).",
                    "affected_sensors": affected_str,
                    "risk_level": "Warning",
                    "timeframe": "Within 1 week"
                }

        elif health_status == "Normal":
            return {
                "priority": "LOW",
                "recommended_action": "Continue Standard Routine Monitoring",
                "reason": "Machinery operates within acceptable operational bounds. Minor noise observed within normal tolerances.",
                "affected_sensors": "None",
                "risk_level": "Normal",
                "timeframe": "Next scheduled maintenance cycle (30 days)"
            }

        else: # Healthy
            return {
                "priority": "LOW",
                "recommended_action": "No Immediate Maintenance Required",
                "reason": "All monitored sensor metrics operate at optimal peak performance levels.",
                "affected_sensors": "None",
                "risk_level": "Optimal",
                "timeframe": "Routine inspection cycle (90 days)"
            }
