import psycopg2
import os
from dotenv import load_dotenv

_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_ENV_PATH)

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT","5432")

def get_db_connection():
    try:
         connection = psycopg2.connect(host=DB_HOST,database=DB_NAME,port=DB_PORT,user=DB_USERNAME,password=DB_PASSWORD)
         return connection
    except Exception as error:
        print("Unable To Connect To Database...",error)
        return None