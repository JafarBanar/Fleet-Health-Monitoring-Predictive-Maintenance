import os
import pandas as pd
import urllib
from sqlalchemy import create_engine
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from prophet import Prophet
import matplotlib.pyplot as plt

# === Azure SQL Setup ===
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE", "fleettelemetrydb")
username = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")
driver = os.getenv("SQL_DRIVER", "{ODBC Driver 17 for SQL Server}")

if not all([server, username, password]):
    raise ValueError("Missing required SQL env vars: SQL_SERVER, SQL_USER, SQL_PASSWORD")

connection_string = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'PORT=1433;'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)

params = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# === Load Data ===
df = pd.read_sql("SELECT * FROM vehicle_telemetry", engine)

# === Fault Prediction with XGBoost ===
print("\n--- XGBoost Fault Prediction ---")
df_fault = df[df['fault_code'].isin([0, 1, 2])].dropna()
X = df_fault[['speed_kmh', 'engine_temp_c', 'battery_voltage_v']]
y = df_fault['fault_code']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)
clf = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
print(classification_report(y_test, preds))

# === Forecasting Engine Temp with Prophet ===
print("\n--- Prophet Forecasting ---")
df_vehicle = df[df['vehicle_id'] == 'V001'][['timestamp', 'engine_temp_c']].copy()
df_vehicle.columns = ['ds', 'y']
df_vehicle = df_vehicle.dropna()

model = Prophet()
model.fit(df_vehicle)
future = model.make_future_dataframe(periods=60, freq='min')
forecast = model.predict(future)

# Save and plot forecast
fig = model.plot(forecast)
fig.savefig("forecast_plot.png")
print("Forecast plot saved as 'forecast_plot.png'")
