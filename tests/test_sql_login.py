import os

import pyodbc
import pandas as pd

# SQL Server connection info
server = os.getenv("SQL_SERVER", "fleetserver2.database.windows.net")
database = os.getenv("SQL_DATABASE", "fleettelemetrydb")
username = os.getenv("SQL_USER", "fleetadmin")
password = os.getenv("SQL_PASSWORD")
driver = os.getenv("SQL_DRIVER", "{ODBC Driver 17 for SQL Server}")

if not password:
    raise RuntimeError("Missing SQL_PASSWORD environment variable.")

# Connection string
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

# Connect and query
conn = pyodbc.connect(conn_str)
df = pd.read_sql("SELECT TOP 10 * FROM vehicle_telemetry", conn)

print("✅ Connected successfully. Sample data:")
print(df.head())
