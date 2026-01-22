import os
from dotenv import load_dotenv

load_dotenv()

DB_SERVER=os.getenv("DB_SERVER","")
DB_NAME=os.getenv("DB_NAME","habitTracker")
DB_TRUSTED_CONNECTION=os.getenv("DB_TRUSTED_CONNECTION","yes").lower()
DB_DRIVER=os.getenv("DB_DRIVER","ODBC Driver 18 for SQL Server")

DB_USER=os.getenv("DB_USER","")
DB_PASSWORD=os.getenv("DB_PASSWORD","")