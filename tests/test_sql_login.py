
import pyodbc
import pandas as pd

# SQL Server connection info
server = "fleetserver2.database.windows.net"
database = "fleettelemetrydb"
username = "fleetadmin"
password = "Fleet@2024"
driver = "{ODBC Driver 17 for SQL Server}"

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
