"""
Root Launcher for MULTI-SENSOR FUSION FOR INTELLIGENT EQUIPMENT HEALTH MONITORING SYSTEM.
Redirects execution to Equipment_Health_Monitoring/app.py.
"""
import os
import sys

# Ensure Equipment_Health_Monitoring directory is in path
project_dir = os.path.join(os.path.dirname(__file__), "Equipment_Health_Monitoring")
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

os.chdir(project_dir)

# Import main application runner
from app import *
