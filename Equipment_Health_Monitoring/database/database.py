"""
SQLite Database manager for schema creation, CRUD queries, and historical telemetry retrieval.
"""
import os
import sqlite3
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

from utils.config import get_data_filepath, load_equipment_config

DEFAULT_DB_PATH = get_data_filepath("equipment_health.db")

class DatabaseManager:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Create database tables if they do not exist and seed initial data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Equipment table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT,
                location TEXT,
                installation_date TEXT,
                rated_power TEXT,
                manufacturer TEXT,
                status TEXT
            )
            """)

            # Sensor Readings table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                equipment_id TEXT NOT NULL,
                temperature REAL,
                vibration REAL,
                pressure REAL,
                humidity REAL,
                current REAL,
                voltage REAL,
                rpm REAL,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            )
            """)

            # Fused Results table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fused_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                equipment_id TEXT NOT NULL,
                composite_risk_score REAL NOT NULL,
                health_score REAL NOT NULL,
                health_status TEXT NOT NULL,
                sensor_contributions_json TEXT,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            )
            """)

            # Anomalies table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                equipment_id TEXT NOT NULL,
                anomaly_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                affected_sensors TEXT NOT NULL,
                description TEXT NOT NULL,
                is_ml_detected INTEGER DEFAULT 0,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            )
            """)

            # Alerts table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                equipment_id TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                acknowledged INTEGER DEFAULT 0,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            )
            """)

            # Maintenance Recommendations table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                equipment_id TEXT NOT NULL,
                priority TEXT NOT NULL,
                recommended_action TEXT NOT NULL,
                reason TEXT NOT NULL,
                affected_sensors TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            )
            """)
            
            conn.commit()

        self._seed_initial_data()

    def _seed_initial_data(self):
        """Seed equipment list and initial historical telemetry if database is empty."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Seed equipment
            cursor.execute("SELECT COUNT(*) FROM equipment")
            if cursor.fetchone()[0] == 0:
                eq_config = load_equipment_config()
                for eq in eq_config.get("equipments", []):
                    cursor.execute("""
                    INSERT INTO equipment (id, name, type, location, installation_date, rated_power, manufacturer, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (eq["id"], eq["name"], eq["type"], eq["location"], eq["installation_date"], eq["rated_power"], eq["manufacturer"], eq["status"]))
                conn.commit()

            # Seed sample sensor data if empty
            cursor.execute("SELECT COUNT(*) FROM sensor_readings")
            if cursor.fetchone()[0] == 0:
                csv_path = get_data_filepath("sample_sensor_data.csv")
                if os.path.exists(csv_path):
                    try:
                        df = pd.read_csv(csv_path)
                        for _, row in df.iterrows():
                            cursor.execute("""
                            INSERT INTO sensor_readings (timestamp, equipment_id, temperature, vibration, pressure, humidity, current, voltage, rpm)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                row["timestamp"], row["equipment_id"], row["temperature"], row["vibration"],
                                row["pressure"], row["humidity"], row["current"], row["voltage"], row["rpm"]
                            ))

                            cursor.execute("""
                            INSERT INTO fused_results (timestamp, equipment_id, composite_risk_score, health_score, health_status, sensor_contributions_json)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                row["timestamp"], row["equipment_id"],
                                (100.0 - row["health_score"]) / 100.0,
                                row["health_score"], row["health_status"],
                                json.dumps({"vibration": 35.0, "temperature": 30.0, "current": 20.0, "pressure": 15.0})
                            ))
                        conn.commit()
                    except Exception as e:
                        print(f"Error seeding database from CSV: {e}")

    def insert_sensor_reading(self, timestamp: str, equipment_id: str, readings: Dict[str, float]) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO sensor_readings (timestamp, equipment_id, temperature, vibration, pressure, humidity, current, voltage, rpm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, equipment_id,
                readings.get("temperature"), readings.get("vibration"), readings.get("pressure"),
                readings.get("humidity"), readings.get("current"), readings.get("voltage"), readings.get("rpm")
            ))
            conn.commit()
            return cursor.lastrowid

    def insert_fused_result(self, timestamp: str, equipment_id: str, composite_risk: float, health_score: float, status: str, contributions: Dict[str, float]) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO fused_results (timestamp, equipment_id, composite_risk_score, health_score, health_status, sensor_contributions_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                timestamp, equipment_id, composite_risk, health_score, status, json.dumps(contributions)
            ))
            conn.commit()
            return cursor.lastrowid

    def insert_anomaly(self, timestamp: str, equipment_id: str, anomaly_type: str, severity: str, affected_sensors: List[str], description: str, is_ml: bool = False) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO anomalies (timestamp, equipment_id, anomaly_type, severity, affected_sensors, description, is_ml_detected)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, equipment_id, anomaly_type, severity, ", ".join(affected_sensors), description, 1 if is_ml else 0
            ))
            conn.commit()
            return cursor.lastrowid

    def insert_alert(self, timestamp: str, equipment_id: str, severity: str, title: str, message: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO alerts (timestamp, equipment_id, severity, title, message)
            VALUES (?, ?, ?, ?, ?)
            """, (timestamp, equipment_id, severity, title, message))
            conn.commit()
            return cursor.lastrowid

    def insert_maintenance_recommendation(self, timestamp: str, equipment_id: str, priority: str, action: str, reason: str, affected_sensors: List[str], timeframe: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO maintenance_recommendations (timestamp, equipment_id, priority, recommended_action, reason, affected_sensors, timeframe)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, equipment_id, priority, action, reason, ", ".join(affected_sensors), timeframe
            ))
            conn.commit()
            return cursor.lastrowid

    def get_recent_sensor_readings(self, equipment_id: str, limit: int = 50) -> pd.DataFrame:
        with self.get_connection() as conn:
            query = """
            SELECT timestamp, temperature, vibration, pressure, humidity, current, voltage, rpm
            FROM sensor_readings
            WHERE equipment_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """
            df = pd.read_sql_query(query, conn, params=(equipment_id, limit))
            if not df.empty:
                df = df.iloc[::-1].reset_index(drop=True)
            return df

    def get_recent_fused_results(self, equipment_id: str, limit: int = 50) -> pd.DataFrame:
        with self.get_connection() as conn:
            query = """
            SELECT timestamp, composite_risk_score, health_score, health_status, sensor_contributions_json
            FROM fused_results
            WHERE equipment_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """
            df = pd.read_sql_query(query, conn, params=(equipment_id, limit))
            if not df.empty:
                df = df.iloc[::-1].reset_index(drop=True)
            return df

    def get_recent_anomalies(self, equipment_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT timestamp, anomaly_type, severity, affected_sensors, description, is_ml_detected
            FROM anomalies
            WHERE equipment_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """, (equipment_id, limit))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_recent_alerts(self, equipment_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, timestamp, severity, title, message, acknowledged
            FROM alerts
            WHERE equipment_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """, (equipment_id, limit))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_latest_recommendation(self, equipment_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT timestamp, priority, recommended_action, reason, affected_sensors, timeframe
            FROM maintenance_recommendations
            WHERE equipment_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """, (equipment_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
