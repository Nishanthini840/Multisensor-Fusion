# Multi-Sensor Fusion for Intelligent Equipment Health Monitoring System

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Ready](https://img.shields.io/badge/GitHub-Ready-success.svg)]()

> A professional, publication-grade Final-Year Engineering Project implementing real-time multi-sensor telemetry fusion, rule-based & ML anomaly detection, explainable equipment health scoring, and predictive maintenance protocols for industrial machinery.

---

## 📌 1. Project Overview

Industrial machinery monitoring relies on multiple heterogeneous sensor channels (temperature, vibration, pressure, humidity, current, voltage, and shaft speed). Evaluating individual sensor thresholds independently often leads to false alarms or missed compound failures. 

This project implements a **Multi-Sensor Fusion Architecture** that validates, normalizes, and fuses 7 distinct physical sensor feeds into a unified **Equipment Health Score (0–100)**. The system features a **Simplicity-First 3-Step Flow Architecture**:

$$\mathbf{INPUT} \longrightarrow \mathbf{MULTI\text{-}SENSOR\ FUSION\ \&\ ANALYSIS} \longrightarrow \mathbf{EQUIPMENT\ HEALTH\ OUTPUT}$$

---

## 🎯 2. Core User Flow

1. **INPUT SECTION**:
   - Accepts 7 physical sensor measurements with explicit units:
     - 🌡️ Temperature (`°C`)
     - 📳 Vibration Severity (`mm/s` RMS)
     - ⏲️ Pressure (`bar`)
     - 💧 Ambient Humidity (`%`)
     - ⚡ Motor Load Current (`A`)
     - 🔌 Supply Voltage (`V`)
     - 🔄 Rotational Speed (`RPM`)
   - Primary action button: **`ANALYZE EQUIPMENT`**
   - Quick preset shortcuts (`Normal`, `Warning`, `Critical`) for rapid testing.

2. **MULTI-SENSOR FUSION & ANALYSIS (PROCESS)**:
   - Evaluates telemetry through sequential processing:
     $$\text{Validation} \longrightarrow \text{Risk Calculation} \longrightarrow \text{Weighted Fusion} \longrightarrow \text{Health Score} \longrightarrow \text{Maintenance Analysis}$$
   - Displays real-time risk indices ($r_i \in [0, 1]$), channel weights ($w_i$), and percentage contributions ($C_i\%$).

3. **EQUIPMENT HEALTH OUTPUT**:
   - **Equipment Health Score**: Prominently calculated score between `0` and `100`.
   - **Equipment Status**: Classified into `Healthy`, `Normal`, `Warning`, or `Critical`.
   - **Main Problem Detected**: Root-cause diagnostic explanation.
   - **Affected Sensors**: Specific channels violating safe operational bounds.
   - **Maintenance Recommendation**: Action protocol, diagnostic rationale, timeframe, and priority.

---

## 🧮 3. Multi-Sensor Fusion & Health Formulation

### 3.1 Risk Normalization ($r_i$)
Each raw sensor measurement $x_i$ is evaluated against domain bounds:
$$r_i(x_i) = \begin{cases} 
0.0 & \text{if } x_i \in [\text{min\_safe}, \text{max\_safe}] \\
0.5 \cdot \frac{x_i - \text{max\_safe}}{\text{warn\_high} - \text{max\_safe}} & \text{if } \text{max\_safe} < x_i < \text{warn\_high} \\
0.5 + 0.5 \cdot \frac{x_i - \text{warn\_high}}{\text{crit\_high} - \text{warn\_high}} & \text{if } \text{warn\_high} \le x_i < \text{crit\_high} \\
1.0 & \text{if } x_i \ge \text{crit\_high}
\end{cases}$$

### 3.2 Weighted Risk Fusion ($R$)
$$\text{Composite Risk } R = \frac{\sum_{i=1}^{N} w_i \cdot r_i}{\sum_{i=1}^{N} w_i}$$

### 3.3 Percentage Risk Contribution ($C_i$)
$$C_i = \left( \frac{w_i \cdot r_i}{\sum w_k r_k} \right) \times 100\%$$

### 3.4 Health Score ($H$)
$$\text{Health Score } H = \max(0, \min(100, (1 - R) \times 100))$$

---

## 📂 4. Project Folder Structure

```
Equipment_Health_Monitoring/
│
├── app.py                             # Main Streamlit application entry point
├── server.py                          # Zero-dependency Python REST API & Web Server
├── requirements.txt                   # Dependency manifest
├── README.md                          # Production-grade technical documentation
├── .gitignore                         # Git exclusion rules
├── .env.example                       # Environment variables template
│
├── pages/                             # 4 Core View Modules
│   ├── __init__.py
│   ├── overview.py                    # 1. Overview Dashboard
│   ├── live_monitoring.py             # 2. Live Monitoring Panel
│   ├── fusion_analysis.py             # 3. Fusion & Health Analysis
│   └── maintenance_history.py         # 4. Maintenance & History
│
├── core/                              # Core Analytical Engines
│   ├── __init__.py
│   ├── sensor_simulator.py            # Physics-aware 7-channel telemetry simulator
│   ├── sensor_fusion.py               # Validation, normalization & fusion
│   ├── health_engine.py               # Health score calculation & status classifier
│   ├── anomaly_detector.py            # Rule-based & ML Isolation Forest detector
│   ├── predictive_maintenance.py      # Actionable maintenance recommendation engine
│   └── alert_engine.py                # Industrial alert generator
│
├── database/                          # SQLite Persistence Layer
│   ├── __init__.py
│   ├── database.py                    # SQLite Manager with auto-schema creation
│   └── models.py                      # Data schema models
│
├── data/                              # Configuration & Seed Data
│   ├── equipment_config.json          # Machinery specs & active equipment registry
│   ├── sensor_thresholds.json         # Operating bounds, weights & units
│   └── sample_sensor_data.csv         # Initial historical dataset
│
├── web/                               # Custom Standalone Web Application
│   ├── index.html                     # 3-Step HTML5 interface
│   ├── css/style.css                  # Modern Light Theme stylesheet
│   └── js/app.js                      # ES6 controller script
│
├── components/                        # Streamlit UI Components
│   ├── __init__.py
│   ├── sidebar.py                     # Minimal control panel
│   ├── metric_cards.py                # KPI cards
│   ├── sensor_cards.py                # Sensor widgets & tables
│   ├── charts.py                      # Plotly charts
│   └── status_components.py          # Status banners & action cards
│
├── utils/                             # Utilities
│   ├── __init__.py
│   ├── config.py                      # JSON configuration loader
│   ├── helpers.py                     # Formatting helpers
│   └── session_manager.py             # Session state manager
│
└── tests/                             # Automated Unit Test Suite
    ├── __init__.py
    ├── test_sensor_fusion.py          # Fusion unit tests
    ├── test_health_engine.py          # Health score unit tests
    └── test_anomaly_detector.py       # Anomaly detector unit tests
```

---

## 💻 5. Installation & Execution Guide

### Prerequisites
- Python 3.9+
- `pip` package manager

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/Equipment_Health_Monitoring.git
cd Equipment_Health_Monitoring
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application

**Option A: Streamlit Interface (Standard Academic Presentation)**
```bash
streamlit run app.py
```

**Option B: Standalone Web Interface (Fast API + HTML5/JS Web App)**
```bash
python server.py 8000
```
Access at `http://localhost:8000`.

---

## 🧪 6. Automated Unit Tests

Run unit tests using Python's built-in `unittest` runner:

```bash
python -m unittest discover -s tests
```

---

## 📤 7. Pushing Project to GitHub

Follow these standard commands to push your project repository to GitHub:

```bash
# 1. Initialize Git repository (if not already done)
git init

# 2. Add all project files
git add .

# 3. Commit changes
git commit -m "Initial commit: Multi-Sensor Fusion for Equipment Health Monitoring System"

# 4. Set main branch
git branch -M main

# 5. Link your GitHub remote repository URL
git remote add origin https://github.com/your-username/your-repo-name.git

# 6. Push code to GitHub
git push -u origin main
```

---

## 📄 8. License

Published under the **MIT License**. Developed for Final-Year Engineering Project Defense.
