import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

print("=" * 60)
print("Q5 — ISOLATION FOREST ANOMALY DETECTION")
print("=" * 60)

print("\nLoading data...")
df = pd.read_excel('newwww.xlsx')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

print(f"Loaded {len(df)} rows and {df.shape[1]} columns")
print(f"Plants: {sorted(df['Plant'].unique())}")
print(f"Machines: {df['MachineID'].nunique()} unique machines")
print(f"Date Range: {df['Timestamp'].min().date()} to {df['Timestamp'].max().date()}")

FEATURES = ['Temperature', 'Vibration', 'Pressure',
            'EnergyConsumption', 'ProductionUnits']

print("\nFeatures used:")
for f in FEATURES:
    print(f"{f}: mean={df[f].mean():.2f}, std={df[f].std():.2f}")

print("\nStandardizing features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[FEATURES])
print("Standardization complete")

print("\nTraining Isolation Forest...")
iso = IsolationForest(n_estimators=200, contamination=0.015,
                      random_state=42, n_jobs=-1)

iso.fit(X_scaled)
df['IF_Score'] = iso.decision_function(X_scaled)
df['IF_Pred'] = iso.predict(X_scaled)

print("Model training complete")

total_anomalies = (df['IF_Pred'] == -1).sum()

print("\nResults:")
print(f"Total rows: {len(df)}")
print(f"Anomalies detected: {total_anomalies}")
print(f"Score range: {df['IF_Score'].min():.4f} to {df['IF_Score'].max():.4f}")

top200 = (
    df[df['IF_Pred'] == -1]
    .sort_values('IF_Score', ascending=True)
    .head(200)[[
        'Timestamp', 'MachineID', 'Plant', 'Temperature',
        'Vibration', 'Pressure', 'EnergyConsumption',
        'ProductionUnits', 'DefectCount', 'IF_Score'
    ]]
    .reset_index(drop=True)
)

top200.index += 1
top200.index.name = 'Anomaly_Rank'

print("\nTop 10 most anomalous readings:\n")

pd.set_option('display.width', 120)
pd.set_option('display.float_format', '{:.4f}'.format)

print(top200[['Timestamp', 'MachineID', 'Plant',
              'Temperature', 'Vibration', 'Pressure',
              'IF_Score']].head(10).to_string())

print("\nAnomalies by plant:")

for plant, count in top200['Plant'].value_counts().items():
    print(f"{plant}: {count}")

top200.to_csv('Q5_Top200_Anomalies.csv')

print("\nSaved to Q5_Top200_Anomalies.csv")
print("Q5 complete")