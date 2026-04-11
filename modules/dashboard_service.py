from database import config
from database import queries

# We should make the connnection to db global so we dont have to define it everytime !

def fetch_number_of_products():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()

    number_of_products = queries.get_number_of_products(cursor) # returns None if no record and tuple if there are records
    if number_of_products is None:
        return {"ok":False,"code":"NO_PRODUCTS","message":"There were no products found!","result":0}
    number_of_products = number_of_products[0]

    return {"ok":True,"code":"SUCCESS","result":number_of_products}


def fetch_total_stocks():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()

    total_stocks = queries.get_total_stocks(cursor)
    if total_stocks is None:
        return {"ok":False,"code":"NO_STOCKS","message":"There were no stocks found!","result":0}
    total_stocks = total_stocks[0]

    return {"ok":True,"code":"SUCCESS","result":total_stocks}

def fetch_low_stock_count():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()

    low_stock_count = queries.get_low_stock_count(cursor,threshold=10)
    low_stock_count = low_stock_count[0]

    return {"ok":True,"code":"SUCCESS","result":low_stock_count}

def fetch_total_revenue():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()

    total_revenue = queries.get_total_revenue(cursor)
    total_revenue = total_revenue[0]

    return {"ok":True,"code":"SUCCESS","result":total_revenue}

def fetch_recent_sales():
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"code":"DB_FAILED","message":"Unable to connect to DB!"}
    cursor = connection.cursor()

    recent_sales = queries.get_recent_sales(cursor) # Returns list of tuples and empty list if no record!
    if not recent_sales:
        return {"ok":False,"code":"NO_SALES_RECORD"}

    return {"ok":True,"code":"SUCCESS","result":recent_sales}