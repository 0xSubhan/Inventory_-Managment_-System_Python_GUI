from database import queries
from database import config
from modules import stock_service

def calculate_total(productName,productQuantity):
    # DB connection
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"message":"DB connection failed!"}
    cursor = connection.cursor()
    # First Validation check : product should exist !
    product = queries.get_product_by_name(cursor,productName)
    if product is None:
        return {"ok":False,"message":"Product Doesn't exist!"}
    # Second Validation check : quantity must be a number and also greater than 0 !
    try:
        productQuantity = int(productQuantity)
        if productQuantity <= 0:
            return {"ok":False,"message":"Quantity must be Positive!"}
    except ValueError:
        return {"ok":False,"message":"Product Must Be A Number!"}
    # Now we get the product price
    productPrice = queries.get_product_price(cursor,productName) # No need to check if product exist because that validation is already done so if no product record exist then it will be caught earlier on ! but maybe for safety we should apply it here to ! maybe later
    productPrice = productPrice[0] # because productPrice returns tuple with only one value which is product pirce !

    total = productQuantity * productPrice
    return {"ok":True,"result":total}

def handle_fetch_transactions():
    connection = config.get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    transactions = queries.get_all_transactions(cursor)
    return transactions

# def fetch_product_name(productID):
#     connection = config.get_db_connection()
#     if connection is None:
#         return
#     cursor = connection.cursor()
#     productName = queries.get_productname_by_id(cursor,productID)
#     return

def fetch_all_transactions():
    transactions = handle_fetch_transactions()
    if not transactions:
        print("No transactions record found")
        return
    # Now we need these list of tuples of transactions in a certain order !
    updated_transactions = []

    for transaction in transactions:
        saleid , productid , quantity , sale_price , total_price , sale_date = transaction

        updated_transactions.append((saleid,sale_date,productid,quantity,sale_price,total_price))

    return updated_transactions

def sell_stock(productName,productQuantity):
    # DB connection
    connection = config.get_db_connection()
    if connection is None:
        return {"ok":False,"message":"DB connection failed!"}
    cursor = connection.cursor()
    # First Validation check : product should exist !
    product = queries.get_product_by_name(cursor,productName)
    if product is None:
        return {"ok":False,"message":"Product Doesn't exist!"}
    # Second Validation check : quantity must be a number and also greater than 0 !
    try:
        productQuantity = int(productQuantity)
        if productQuantity <= 0:
            return {"ok":False,"message":"Quantity must be Positive!"}
    except ValueError:
        return {"ok":False,"message":"Product Must Be A Number!"}
    # Now we get the product price
    productPrice = queries.get_product_price(cursor,productName) # No need to check if product exist because that validation is already done so if no product record exist then it will be caught earlier on ! but maybe for safety we should apply it here to ! maybe later
    productPrice = productPrice[0] # because productPrice returns tuple with only one value which is product pirce !

    sell_total = productQuantity * productPrice

    productID = queries.get_productID_by_productName(cursor,productName)

    # Validation : the product should have greater or equal to selling price !
    product_units = queries.get_product_quantity(cursor,productID)
    product_units = product_units[0]
    product_total = product_units * productPrice
    if sell_total > product_total:
        return {"ok": False, "message": "Not Enough Stock"}


    stock_service.apply_stock_change(productID,productQuantity,"OUT")
    queries.insert_sale_transaction(cursor,productID,productQuantity,productPrice,sell_total)

    cursor.close()
    connection.commit()
    connection.close()


    return {"ok": True, "message": "Transaction Successfull!"}

