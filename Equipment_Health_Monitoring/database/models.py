"""
Data models and schemas for SQLite entities.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class Equipment:
    id: str
    name: str
    type: str
    location: str
    installation_date: str
    rated_power: str
    manufacturer: str
    status: str

@dataclass
class SensorReadingRecord:
    timestamp: str
    equipment_id: str
    temperature: float
    vibration: float
    pressure: float
    humidity: float
    current: float
    voltage: float
    rpm: float
    id: Optional[int] = None

@dataclass
class FusedResultRecord:
    timestamp: str
    equipment_id: str
    composite_risk_score: float
    health_score: float
    health_status: str
    sensor_contributions_json: str
    id: Optional[int] = None

@dataclass
class AnomalyRecord:
    timestamp: str
    equipment_id: str
    anomaly_type: str
    severity: str
    affected_sensors: str
    description: str
    is_ml_detected: bool
    id: Optional[int] = None

@dataclass
class AlertRecord:
    timestamp: str
    equipment_id: str
    severity: str
    title: str
    message: str
    acknowledged: bool = False
    id: Optional[int] = None

@dataclass
class MaintenanceRecommendationRecord:
    timestamp: str
    equipment_id: str
    priority: str
    recommended_action: str
    reason: str
    affected_sensors: str
    timeframe: str
    id: Optional[int] = None
