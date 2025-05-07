
import pandas as pd
import pyodbc

# Load CSV data
df = pd.read_csv("telemetry_data.csv")

# SQL Server connection info
server = "fleetserver2.database.windows.net"
database = "fleettelemetrydb"
username = "fleetadmin"
password = "Fleet@2024"
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

# Connect and upload data
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Insert data row by row (safe for smaller CSVs)
insert_query = '''
    INSERT INTO vehicle_telemetry (
        timestamp, vehicle_id, speed_kmh, engine_temp_c, battery_voltage_v, fault_code, location_lat, location_lon
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''

for _, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("✅ Data uploaded successfully to vehicle_telemetry.")
