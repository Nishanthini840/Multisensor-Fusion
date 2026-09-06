"""
Multi-Sensor Fusion Industrial Control Center - Web Backend Server.
Zero-dependency HTTP API & Static File Web Server.
"""
import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

# Add project root directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.config import load_equipment_config
from database.database import DatabaseManager
from core.sensor_simulator import SensorSimulator
from core.sensor_fusion import SensorFusionEngine
from core.health_engine import EquipmentHealthEngine
from core.anomaly_detector import AnomalyDetector
from core.predictive_maintenance import PredictiveMaintenanceEngine
from core.alert_engine import AlertEngine

DB = DatabaseManager()
SIMULATOR = SensorSimulator()
FUSION_ENGINE = SensorFusionEngine()
HEALTH_ENGINE = EquipmentHealthEngine()
ANOMALY_DETECTOR = AnomalyDetector(ml_enabled=True)
MAINTENANCE_ENGINE = PredictiveMaintenanceEngine()
ALERT_ENGINE = AlertEngine()

# Current Input State
CURRENT_INPUTS = {
    "temperature": 42.5,
    "vibration": 1.8,
    "pressure": 4.1,
    "humidity": 45.0,
    "current": 12.4,
    "voltage": 401.2,
    "rpm": 1480.0
}

def analyze_sensors(inputs_dict):
    """Run core multi-sensor fusion pipeline on explicit input vector."""
    equipment_id = "EQ-IND-101"

    # 1. Validation & Fusion
    fusion_result = FUSION_ENGINE.process_fusion(inputs_dict)

    # 2. Health Engine Evaluation
    health_result = HEALTH_ENGINE.evaluate(fusion_result)

    # 3. Anomaly Detection
    anomalies = ANOMALY_DETECTOR.detect_all(fusion_result["cleaned_readings"])

    # 4. Predictive Maintenance Recommendation
    recommendation = MAINTENANCE_ENGINE.evaluate_recommendation(
        health_score=health_result["health_score"],
        health_status=health_result["status"],
        cleaned_readings=fusion_result["cleaned_readings"],
        normalized_risks=fusion_result["normalized_risks"],
        anomalies=anomalies
    )

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Persist analysis tick to SQLite DB
    try:
        DB.insert_sensor_reading(now_str, equipment_id, fusion_result["cleaned_readings"])
        DB.insert_fused_result(
            now_str, equipment_id,
            fusion_result["composite_risk"],
            health_result["health_score"],
            health_result["status"],
            fusion_result["contributions"]
        )
    except Exception:
        pass

    # Extract Main Problem & Affected Sensors
    risk_factors = health_result["risk_factors"]
    if risk_factors:
        main_problem = risk_factors[0]["reason"]
        affected_sensors = ", ".join([rf["sensor"] for rf in risk_factors])
    elif anomalies:
        main_problem = anomalies[0]["description"]
        affected_sensors = anomalies[0].get("sensor", "Multi-Sensor Pattern")
    else:
        main_problem = "None (All sensor parameters operating within nominal safe bounds)"
        affected_sensors = "None"

    return {
        "timestamp": now_str,
        "inputs": fusion_result["cleaned_readings"],
        "normalized_risks": fusion_result["normalized_risks"],
        "weights": fusion_result["weights"],
        "composite_risk": fusion_result["composite_risk"],
        "contributions": fusion_result["contributions"],
        "health_score": health_result["health_score"],
        "health_status": health_result["status"],
        "main_problem": main_problem,
        "affected_sensors": affected_sensors,
        "recommendation": recommendation.get("recommended_action", "Routine Inspection"),
        "reason": recommendation.get("reason", "All parameters nominal."),
        "timeframe": recommendation.get("timeframe", "Routine cycle"),
        "priority": recommendation.get("priority", "LOW")
    }

class TelemetryAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        web_dir = os.path.join(PROJECT_ROOT, "web")
        super().__init__(*args, directory=web_dir, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/status" or path == "/api/analyze":
            self.send_json_response(analyze_sensors(CURRENT_INPUTS))
        elif path == "/api/preset":
            query = urllib.parse.parse_qs(parsed_path.query)
            mode = query.get("mode", ["normal"])[0]
            readings = SIMULATOR._get_baseline_state(mode)
            CURRENT_INPUTS.update(readings)
            self.send_json_response(analyze_sensors(CURRENT_INPUTS))
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/analyze":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                data = json.loads(post_body.decode("utf-8"))
                for k in CURRENT_INPUTS:
                    if k in data:
                        CURRENT_INPUTS[k] = float(data[k])
                self.send_json_response(analyze_sensors(CURRENT_INPUTS))
            except Exception as e:
                self.send_json_response({"error": str(e)}, status=400)
        else:
            self.send_error(404, "Endpoint not found")

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, TelemetryAPIHandler)
    print(f"Multi-Sensor Fusion Control Center Web App running on http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
