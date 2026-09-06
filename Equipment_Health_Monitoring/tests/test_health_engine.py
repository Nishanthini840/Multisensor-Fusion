"""
Unit tests for core/health_engine.py
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.health_engine import EquipmentHealthEngine

class TestHealthEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EquipmentHealthEngine()

    def test_health_score_calculation(self):
        self.assertEqual(self.engine.calculate_health_score(0.0), 100.0)
        self.assertEqual(self.engine.calculate_health_score(1.0), 0.0)
        self.assertEqual(self.engine.calculate_health_score(0.25), 75.0)

    def test_status_classification(self):
        self.assertEqual(self.engine.classify_status(95.0), "Healthy")
        self.assertEqual(self.engine.classify_status(80.0), "Normal")
        self.assertEqual(self.engine.classify_status(55.0), "Warning")
        self.assertEqual(self.engine.classify_status(25.0), "Critical")

if __name__ == "__main__":
    unittest.main()
