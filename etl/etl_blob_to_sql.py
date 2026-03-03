import os
import pandas as pd
from azure.storage.blob import BlobServiceClient
from sqlalchemy import create_engine
import urllib

# === Azure Blob Storage Setup ===
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "raw-telemetry")
BLOB_FILE_NAME = os.getenv("BLOB_FILE_NAME", "telemetry_data.csv")

if not BLOB_CONNECTION_STRING:
    raise ValueError("Missing required env var: BLOB_CONNECTION_STRING")

# Download CSV from Blob
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=BLOB_FILE_NAME)
download_stream = blob_client.download_blob()
df = pd.read_csv(download_stream)

# === Optional Data Cleaning ===
# Example: drop rows with missing timestamps
df.dropna(subset=["timestamp"], inplace=True)

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

# === Upload Data to Azure SQL ===
df.to_sql("vehicle_telemetry", engine, if_exists="append", index=False)
print("Data successfully inserted into Azure SQL.")
