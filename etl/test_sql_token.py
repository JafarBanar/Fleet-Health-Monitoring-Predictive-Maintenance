import pandas as pd
import sqlalchemy
import subprocess
import json

# Step 1: Get access token from Azure CLI
token_raw = subprocess.check_output([
    "az", "account", "get-access-token", "--resource", "https://database.windows.net/"
])
access_token = json.loads(token_raw)["accessToken"]

# Step 2: Create SQLAlchemy connection using pytds with token
server = "fleetserver1.database.windows.net"
database = "fleettelemetrydb"

engine = sqlalchemy.create_engine(
    f"mssql+pytds://@{server}:1433/{database}",
    connect_args={
        "authtoken": access_token
    }
)

# Step 3: Query with pandas
with engine.connect() as conn:
    df = pd.read_sql("SELECT TOP 10 * FROM vehicle_telemetry", conn)

print(df.head())
