import psycopg2
import os

def get_db_connection():
    """
    Create a connection to the Postgres database.
    Reads credentials from environment variables (set in docker-compose.yml or shell).
    Returns a psycopg2 connection object.
    """
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 5432)),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )