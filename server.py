"""
Root Launcher for MULTI-SENSOR FUSION FOR INTELLIGENT EQUIPMENT HEALTH MONITORING SYSTEM.
Runs the Python HTTP API & Web Control Center Server.
"""
import os
import sys

project_dir = os.path.join(os.path.dirname(__file__), "Equipment_Health_Monitoring")
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

os.chdir(project_dir)

from server import run_server

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
