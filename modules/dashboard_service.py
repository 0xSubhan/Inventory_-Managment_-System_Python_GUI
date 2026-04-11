from database import config
from database import queries

# We should make the connnection to db global so we dont have to define it everytime !

def fetch_number_of_products():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()
    try:
        number_of_products = queries.get_number_of_products(cursor) # returns None if no record and tuple if there are records
        if number_of_products is None:
            return {"ok":False,"code":"NO_PRODUCTS","message":"There were no products found!","result":0}
        number_of_products = number_of_products[0]

        return {"ok":True,"code":"SUCCESS","result":number_of_products}
    finally:
        cursor.close()
        connection.close()


def fetch_total_stocks():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()
    try:
        total_stocks = queries.get_total_stocks(cursor)
        if total_stocks is None or total_stocks[0] is None:
            return {"ok":False,"code":"NO_STOCKS","message":"There were no stocks found!","result":0}
        total_stocks = total_stocks[0]

        return {"ok":True,"code":"SUCCESS","result":total_stocks}
    finally:
        cursor.close()
        connection.close()

def fetch_low_stock_count():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()
    try:
        low_stock_count = queries.get_low_stock_count(cursor,threshold=10)
        if low_stock_count is None:
            return {"ok":False,"code":"NO_LOW_STOCK","message":"Could not fetch low stock count.","result":0}
        low_stock_count = low_stock_count[0]

        return {"ok":True,"code":"SUCCESS","result":low_stock_count}
    finally:
        cursor.close()
        connection.close()

def fetch_total_revenue():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()
    try:
        total_revenue = queries.get_total_revenue(cursor)
        if total_revenue is None or total_revenue[0] is None:
            return {"ok":False,"code":"NO_REVENUE","message":"There were no sales found!","result":0}
        total_revenue = total_revenue[0]

        return {"ok":True,"code":"SUCCESS","result":total_revenue}
    finally:
        cursor.close()
        connection.close()

def fetch_recent_sales():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()
    try:
        recent_sales = queries.get_recent_sales(cursor) # Returns list of tuples and empty list if no record!
        if not recent_sales:
            return {"ok":False,"code":"NO_SALES_RECORD"}

        return {"ok":True,"code":"SUCCESS","result":recent_sales}
    finally:
        cursor.close()
        connection.close()
