import tkinter as tk
from database import queries , config
from modules import product_service

def restock(productID,stock_quantity,movement_type): # This function maybe can be used in sales too ???
    # first fill the movement table by query
    connection = config.get_db_connection()
    if connection is None:
        print("DB CONNECTION FAIILED")
        return
    cursor = connection.cursor()
    queries.insert_movement(cursor,productID,stock_quantity,movement_type)
    # Change the product table quantity
    queries.increase_quantity(cursor,stock_quantity,productID)
    # Close the db here !
    cursor.close()
    connection.commit()
    connection.close()

    return {"ok":True,"code":"Success","message":"Stock Updated!"}

def fetch_productID(product_Name):
    connection = config.get_db_connection()
    if connection is None:
        print("Db connection failed") # Test Case
        return
    cursor = connection.cursor()

    result = queries.get_productID_by_productName(cursor,product_Name)
    cursor.close()
    connection.commit()
    connection.close()

    return result

def handle_fetch_products():
    connection = config.get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()

    products = queries.get_all_products(cursor)
    return products # Empty list if no record otherwise list of tuples

def fetch_products_with_stocklvl(threshold=10):
    products = handle_fetch_products()
    if not products:
        print("No records found")
        return

    products_with_stock_lvl = []

    # Now we have list of tuples where each tuple represent a record !
    for product in products:
        productid , name , category , price , quantity , _ = product
        stock_lvl = "HIGH" if quantity >= threshold else "LOW"
        products_with_stock_lvl.append((productid,name,category,price,quantity,stock_lvl))

    return products_with_stock_lvl

def fetch_product(product_name):
    connection = config.get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    product = queries.get_product_by_name(cursor,product_name) # Return None if no record is found !

    return product


def upgrade_stock(entries):
    product_name = entries['name'].get().strip().lower()
    quantity = entries['stock'].get().strip()
    product_id = fetch_productID(product_name) # it returns tuple with only id
    # Validation Check: If product doesnt exist !
    if product_id is None:
        print("Product does'nt exist!")
        return {"ok":False,"code":"VALIDATION_ERROR","message":"Product Does't exist!"}

    product_id = product_id[0] # so we extract the value from the tuple

    # Quantity must be a number, Positive Number , Not Decimal!
    try:
        quantity = int(quantity)
    except:
        print("This mean user entered value other than int")
        return {"ok":False,"code":"VALIDATION_ERROR","message":"Quantity must be a number!"}
    # Validation Check : Quantity should be greater than 0 !
    if quantity <= 0:
        print("Quantity is less than 0") # Test Case
        return {"ok":False,"code":"VALIDATION_ERROR","message":"Quantity must be greater than 0!"}

    # For product to restock , the product should exist !
    product_record = product_service.find_product_by_name(product_name) # Return true if product exist else return None
    if product_record is None:
        print("Record Doesnt exist so cant restock") # Test Case
        return
    # Restock
    return restock(product_id,quantity,"IN")