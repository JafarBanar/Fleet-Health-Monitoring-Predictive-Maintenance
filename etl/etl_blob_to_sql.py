
import pandas as pd
from azure.storage.blob import BlobServiceClient
from sqlalchemy import create_engine
import urllib

# === Azure Blob Storage Setup ===
BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=<YOUR_ACCOUNT_NAME>;AccountKey=<YOUR_ACCOUNT_KEY>;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME = "raw-telemetry"
BLOB_FILE_NAME = "telemetry_data.csv"

# Download CSV from Blob
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=BLOB_FILE_NAME)
download_stream = blob_client.download_blob()
df = pd.read_csv(download_stream)

# === Optional Data Cleaning ===
# Example: drop rows with missing timestamps
df.dropna(subset=["timestamp"], inplace=True)

# === Azure SQL Setup ===
server = '<YOUR_SQL_SERVER>.database.windows.net'
database = 'fleettelemetrydb'
username = '<YOUR_USERNAME>'
password = 'YOUR_PASSWORD'  # For production, use environment variables or secrets manager
driver = '{ODBC Driver 17 for SQL Server}'

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
