import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("SQL_SERVER")
username = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")


# SQL Server connection info
database = "fleettelemetrydb"
driver = "{ODBC Driver 17 for SQL Server}"

# Build connection string
conn_str = (
    f"Driver={driver};"
    f"Server=tcp:{server},1433;"
    f"Database={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Connect and load data
conn = pyodbc.connect(conn_str)
df = pd.read_sql("SELECT * FROM vehicle_telemetry", conn)

# Streamlit UI
st.set_page_config(page_title="Fleet Health Dashboard", layout="wide")
st.title("🚚 Fleet Health Monitoring Dashboard")

st.subheader("📊 Summary")
st.metric("Total Vehicles", df['vehicle_id'].nunique())
st.metric("Total Records", len(df))
st.metric("Critical Faults", (df['fault_code'] == 2).sum())

vehicle_ids = df['vehicle_id'].unique()
selected_vehicle = st.selectbox("Select Vehicle ID", vehicle_ids)
df_vehicle = df[df['vehicle_id'] == selected_vehicle]

st.subheader("📈 Speed and Engine Temperature Over Time")

fig, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(df_vehicle['timestamp'], df_vehicle['speed_kmh'], label="Speed (km/h)", color="blue")
ax1.set_ylabel("Speed (km/h)", color="blue")

ax2 = ax1.twinx()
ax2.plot(df_vehicle['timestamp'], df_vehicle['engine_temp_c'], label="Engine Temp (°C)", color="red")
ax2.set_ylabel("Engine Temp (°C)", color="red")

fig.autofmt_xdate()  # Rotate x-axis labels to avoid overlap
st.pyplot(fig)


# Optional anomaly section
st.subheader("🚨 Anomaly Alerts")
df_anomaly = df_vehicle[df_vehicle['engine_temp_c'] > 110]
if not df_anomaly.empty:
    st.warning(f"{len(df_anomaly)} high-temp anomalies detected for {selected_vehicle}")
    st.dataframe(df_anomaly)
else:
    st.success("No high-temperature anomalies detected.")



#streamlit run streamlit_app.py --server.port 8502