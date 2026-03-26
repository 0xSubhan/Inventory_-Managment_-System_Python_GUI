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

    # change the product table quantity
    queries.increase_quantity(cursor,stock_quantity,productID)

    # Table refresh maybe

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


def upgrade_stock(entries):
    product_name = entries['name'].get().strip().lower()
    quantity = int(entries['stock'].get().strip())
    product_id = fetch_productID(product_name) # it returns tuple with only id
    product_id = product_id[0] # so we extract the value from the tuple

    if quantity < 0:
        print("Quantity is less than 0") # Test Case
        return

    # For product to restock , the product should exist !
    product_record = product_service.find_product_by_name(product_name) # Return true if product exist else return None
    if product_record is None:
        print("Record Doesnt exist so cant restock") # Test Case
        return

    # Restock
    return restock(product_id,quantity,"IN")