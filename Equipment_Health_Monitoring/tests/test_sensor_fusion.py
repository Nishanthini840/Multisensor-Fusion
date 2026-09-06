"""
Unit tests for core/sensor_fusion.py
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.sensor_fusion import SensorFusionEngine, WeightedRiskFusionStrategy

class TestSensorFusionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SensorFusionEngine()

    def test_missing_value_imputation(self):
        raw_readings = {
            "temperature": 45.0,
            "vibration": None,
            "pressure": 4.0,
            "humidity": 50.0,
            "current": 12.0,
            "voltage": 400.0,
            "rpm": None
        }
        cleaned = self.engine.validate_and_clean_readings(raw_readings)
        self.assertIsNotNone(cleaned["vibration"])
        self.assertIsNotNone(cleaned["rpm"])
        self.assertIsInstance(cleaned["vibration"], float)

    def test_sensor_normalization(self):
        # Nominal temperature (40 °C) -> risk should be 0.0
        risk_nominal = self.engine.normalize_sensor_risk("temperature", 40.0)
        self.assertEqual(risk_nominal, 0.0)

        # Critical temperature (95 °C) -> risk should be 1.0
        risk_critical = self.engine.normalize_sensor_risk("temperature", 95.0)
        self.assertEqual(risk_critical, 1.0)

    def test_fusion_pipeline(self):
        raw_readings = {
            "temperature": 45.0,
            "vibration": 2.0,
            "pressure": 4.0,
            "humidity": 50.0,
            "current": 12.0,
            "voltage": 400.0,
            "rpm": 1475.0
        }
        result = self.engine.process_fusion(raw_readings)
        self.assertIn("composite_risk", result)
        self.assertIn("contributions", result)
        self.assertGreaterEqual(result["composite_risk"], 0.0)
        self.assertLessEqual(result["composite_risk"], 1.0)

if __name__ == "__main__":
    unittest.main()
