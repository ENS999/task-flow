import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

class Database():
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            self.connection = psycopg2.connect(database_url, sslmode="require")
        else:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                sslmode=os.getenv("DB_SSLMODE", "prefer")
            )

    def get_cursor(self):
        return self.connection.cursor(cursor_factory=RealDictCursor)
    
    def close(self):
        self.connection.close()