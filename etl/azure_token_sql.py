import pyodbc
import pandas as pd
import subprocess
import json

# Step 1: Get access token from Azure CLI
token_raw = subprocess.check_output([
    "az", "account", "get-access-token", "--resource", "https://database.windows.net/"
])
access_token = json.loads(token_raw)["accessToken"]

# Step 2: Setup connection string
server = "fleetserver1.database.windows.net"
database = "fleettelemetrydb"

conn_str = (
    f"Driver={{ODBC Driver 17 for SQL Server}};"
    f"Server=tcp:{server},1433;"
    f"Database={database};"
    f"Authentication=ActiveDirectoryAccessToken"
)

# Step 3: Connect with token (1256 = SQL_COPT_SS_ACCESS_TOKEN)
conn = pyodbc.connect(conn_str, attrs_before={1256: access_token})
df = pd.read_sql("SELECT * FROM vehicle_telemetry", conn)

# Step 4: Use the data
print(df.head())
