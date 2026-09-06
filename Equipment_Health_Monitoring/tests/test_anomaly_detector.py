"""
Unit tests for core/anomaly_detector.py
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.anomaly_detector import AnomalyDetector

class TestAnomalyDetector(unittest.TestCase):
    def setUp(self):
        self.detector = AnomalyDetector(ml_enabled=False)

    def test_rule_based_breach(self):
        readings = {
            "temperature": 95.0,  # Critical high breach
            "vibration": 2.0,
            "pressure": 4.0,
            "humidity": 50.0,
            "current": 12.0,
            "voltage": 400.0,
            "rpm": 1475.0
        }
        anomalies = self.detector.detect_rule_based_anomalies(readings)
        self.assertTrue(len(anomalies) > 0)
        self.assertEqual(anomalies[0]["severity"], "CRITICAL")

if __name__ == "__main__":
    unittest.main()
