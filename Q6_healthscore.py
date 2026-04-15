import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import warnings

warnings.filterwarnings('ignore')

print("=" * 60)
print("Q6 — HEALTHSCORE REGRESSION")
print("=" * 60)

print("\nLoading data...")
df = pd.read_excel('newwww.xlsx')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
print(f"Loaded {len(df)} rows")

print("\nEngineering features...")

df['EnergyPerUnit'] = df['EnergyConsumption'] / df['ProductionUnits'].clip(lower=1)
df['DefectRate'] = df['DefectCount'] / df['ProductionUnits'].clip(lower=1)

print(f"EnergyPerUnit mean: {df['EnergyPerUnit'].mean():.3f}")
print(f"DefectRate mean: {df['DefectRate'].mean():.4f}")

print("\nBuilding HealthScore...")

stress_cols = ['Temperature','Vibration','Pressure','EnergyPerUnit','DefectRate']
weights = [0.30, 0.25, 0.20, 0.15, 0.10]

scaler = StandardScaler()
Z = pd.DataFrame(
    scaler.fit_transform(df[stress_cols]),
    columns=[f'Z_{c}' for c in stress_cols]
)

df['RawStress'] = sum(w * Z[f'Z_{c}'] for w, c in zip(weights, stress_cols))
df['HealthScore'] = (50 - 10 * df['RawStress']).clip(0, 100)

print(f"Mean: {df['HealthScore'].mean():.2f}")
print(f"Std: {df['HealthScore'].std():.2f}")
print(f"Min: {df['HealthScore'].min():.2f}")
print(f"Max: {df['HealthScore'].max():.2f}")

print("\nTraining model...")

FEATURES = ['Temperature','Vibration','Pressure',
            'EnergyConsumption','ProductionUnits',
            'DefectCount','MaintenanceFlag',
            'EnergyPerUnit','DefectRate']

X = df[FEATURES]
y = df['HealthScore']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.8,
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nModel performance:")
print(f"R2 Score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

print("\nFeature importance:")

importance_df = pd.DataFrame({
    'Feature': FEATURES,
    'Importance': model.feature_importances_,
    'Importance%': (model.feature_importances_ * 100).round(2)
}).sort_values('Importance%', ascending=False).reset_index(drop=True)

importance_df.index += 1

for _, row in importance_df.iterrows():
    print(f"{int(row.name)}. {row['Feature']} {row['Importance%']:.2f}%")

df[['Timestamp','MachineID','Plant','HealthScore']].to_csv(
    'Q6_HealthScores.csv', index=False)

importance_df[['Feature','Importance%']].to_csv(
    'Q6_Feature_Importance.csv', index=False)

print("\nSaved outputs")
print("Q6 complete")