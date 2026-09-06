"""
Alert Engine for generating timestamped industrial notification alerts.
"""
from typing import Dict, Any, List
from datetime import datetime

class AlertEngine:
    def process_alerts(
        self,
        health_score: float,
        health_status: str,
        anomalies: List[Dict[str, Any]],
        equipment_id: str
    ) -> List[Dict[str, Any]]:
        """
        Generate list of active alert objects based on equipment condition.
        """
        alerts = []
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Health status level alerts
        if health_status == "Critical":
            alerts.append({
                "timestamp": now_str,
                "equipment_id": equipment_id,
                "severity": "CRITICAL",
                "title": "Critical Equipment Condition",
                "message": f"Equipment health score dropped to {health_score}/100. Immediate maintenance attention required."
            })
        elif health_status == "Warning":
            alerts.append({
                "timestamp": now_str,
                "equipment_id": equipment_id,
                "severity": "WARNING",
                "title": "Equipment Warning Status",
                "message": f"Equipment health score at {health_score}/100. Operational parameters degrading."
            })

        # Anomaly-triggered alerts
        for anomaly in anomalies:
            alerts.append({
                "timestamp": now_str,
                "equipment_id": equipment_id,
                "severity": anomaly["severity"],
                "title": f"Anomaly: {anomaly['type']}",
                "message": anomaly["description"]
            })

        return alerts
