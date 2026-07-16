import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

try:
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )
    print("Connected to RDS")
    conn.close()
except Exception as e:
    print("Failed:", e)