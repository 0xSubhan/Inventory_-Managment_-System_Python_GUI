from database import config
from database import queries


def handle_fetching_low_stock_records():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"message":"DB connection failed!"}
    cursor = connection.cursor()
    records = queries.get_low_stock_records(cursor)
    return records


def fetch_low_stock_records():
    records = handle_fetching_low_stock_records()

    if not records:
        return {"ok":False,"message":"No Record With Low Stock Found!"}

    return {"ok":True,"result":records}