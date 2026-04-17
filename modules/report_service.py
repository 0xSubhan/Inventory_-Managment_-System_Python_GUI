from database import config
from database import queries
from datetime import datetime

def validate_date_range(from_date,to_date):
    if not from_date or not to_date:
        return {"ok":False,"code":"VALIDATION_ERROR","message":"Both dates are required. Use YYYY-MM-DD format."}
    try:
        from_date_obj = datetime.strptime(from_date,"%Y-%m-%d").date()
        to_date_obj = datetime.strptime(to_date,"%Y-%m-%d").date()
    except ValueError:
        return {"ok":False,"code":"VALIDATION_ERROR","message":"Invalid date format. Use YYYY-MM-DD."}

    if from_date_obj > to_date_obj:
        return {"ok":False,"code":"VALIDATION_ERROR","message":"From date cannot be after To date."}
    return {"ok":True}

def fetch_low_stock_records(threshold=10):
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}

    cursor = connection.cursor()
    try:
        records = queries.get_low_stock_products(cursor,threshold=threshold)
        if not records:
            return {"ok":False,"code":"NO_LOW_STOCK","message":"No low stock products found!"}
        return {"ok":True,"code":"SUCCESS","result":records}
    finally:
        cursor.close()
        connection.close()

def fetch_top_products(limit=5):
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}

    cursor = connection.cursor()
    try:
        top_products = queries.get_top_five_products(cursor,limit=limit)
        if not top_products:
            return {"ok":False,"code":"NO_PRODUCTS","message":"No sales records found for top products!"}
        return {"ok":True,"code":"SUCCESS","result":top_products}
    finally:
        cursor.close()
        connection.close()

def fetch_sales_records_by_date(from_date,to_date):
    validation = validate_date_range(from_date,to_date)
    if not validation["ok"]:
        return validation

    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}

    cursor = connection.cursor()
    try:
        records = queries.get_transactions_by_date_range(cursor,from_date,to_date)
        if not records:
            return {"ok":False,"code":"NO_SALES_RECORD","message":"No sales records found in the selected date range."}
        return {"ok":True,"code":"SUCCESS","result":records}
    finally:
        cursor.close()
        connection.close()

def fetch_top_products_by_date(from_date,to_date,limit=5):
    validation = validate_date_range(from_date,to_date)
    if not validation["ok"]:
        return validation

    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}

    cursor = connection.cursor()
    try:
        top_products = queries.get_top_five_products_by_date_range(cursor,from_date,to_date,limit=limit)
        if not top_products:
            return {"ok":False,"code":"NO_PRODUCTS","message":"No top products found in the selected date range."}
        return {"ok":True,"code":"SUCCESS","result":top_products}
    finally:
        cursor.close()
        connection.close()
