import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def test_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            ssl_ca=os.getenv("SSL_CA"),
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )
        print("Database connection successful!")
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

test_db_connection()
