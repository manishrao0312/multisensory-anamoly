# 🏭 Industrial Sensor Monitoring & Anomaly Detection

A comprehensive data analytics pipeline for industrial IoT sensor data — covering anomaly detection, health scoring, SQL-based reporting, Excel dashboards, and Power BI visualizations.

---

## 📁 Repository Structure

```
├── Q1_Q2.xlsx                    # Excel analysis — EDA, anomaly flags, pivot dashboards
├── Q3_Q4_SQL (1).sql             # SQL queries — reporting, aggregations, anomaly queries
├── Q5_anomaly_detection.py       # Isolation Forest anomaly detection model
├── Q6_healthscore.py             # Gradient Boosting machine health score model
└── SensorMonitoring_Dashboard.pbix  # Power BI interactive dashboard
```

---

## 📊 Project Overview

This project analyzes **20,000 hourly sensor readings** across **3 plants** and **50 machines** (Q1–Q2 2024), performing end-to-end analytics from raw data ingestion to predictive health scoring.

### Dataset
- **Scope:** 3 plants (Plant_A, Plant_B, Plant_C), 50 machines each
- **Period:** Q1–Q2 2024 (~20,000 records)
- **Sensors:** Temperature, Vibration, Pressure, RPM, Energy Consumption

---

## 🔍 Key Findings

| Metric | Result |
|---|---|
| Total anomalies flagged (±3σ) | **158** |
| Worst performing machine | **Machine 126, Plant_C** (CI = 0.1200) |
| Isolation Forest anomalies | **300** (contamination = 0.015) |
| Health Score model R² | **0.9963** |

---

## 🧩 Components

### Q1 & Q2 — Excel Analysis (`Q1_Q2.xlsx`)
- Exploratory Data Analysis (EDA) with summary statistics
- Z-score based anomaly flagging (±3σ threshold → **158 anomalies**)
- Machine-level Composite Index (CI) ranking
- Pivot table dashboards and trend charts

### Q3 & Q4 — SQL Reporting (`Q3_Q4_SQL (1).sql`)
- Sensor-level aggregations per plant and machine
- Anomaly summary queries using statistical thresholds
- Downtime and efficiency reporting
- Cross-plant comparative analysis

### Q5 — Anomaly Detection (`Q5_anomaly_detection.py`)
- **Model:** Isolation Forest (scikit-learn)
- **Contamination:** 0.015
- **Output:** 300 anomalous readings flagged
- Features: Temperature, Vibration, Pressure, RPM, Energy Consumption

### Q6 — Health Score Model (`Q6_healthscore.py`)
- **Model:** GradientBoostingRegressor
- **R² Score:** 0.9963
- Predicts a continuous machine health score (0–100)
- Feature importance analysis included

### Power BI Dashboard (`SensorMonitoring_Dashboard.pbix`)
- Plant-wise KPI cards and anomaly heatmaps
- Machine health trend lines
- Drill-through filtering by plant, machine, and time period

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python (pandas, scikit-learn) | Anomaly detection & health scoring |
| SQL | Data querying & reporting |
| Microsoft Excel | EDA, pivot analysis, dashboards |
| Power BI | Interactive visual dashboards |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

### Run Anomaly Detection
```bash
python Q5_anomaly_detection.py
```

### Run Health Score Model
```bash
python Q6_healthscore.py
```

### SQL
Run `Q3_Q4_SQL (1).sql` against your database containing the sensor readings table.

---

## 👤 Author

**Manish Rao**  
B.E. Computer Science | SMVITM, Udupi  
Data Analysis & AI Intern @ Incanto Dynamics, Bangalore  
[GitHub](https://github.com/manishrao0312)

---

## 📄 License

This project is for academic and internship demonstration purposes.
