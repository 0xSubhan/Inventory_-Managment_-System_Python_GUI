import tkinter as tk
from database import queries
from database import config
from database.queries import get_product_by_name

def find_product_by_name(name):
    connection = config.get_db_connection()
    if connection is None:
        print("Save product terminated")  # Test case
        return False

    cursor = connection.cursor()
    product = get_product_by_name(cursor,name)

    cursor.close()
    connection.close()
    return product

def add_product(name,category,price,quantity):
    connection = config.get_db_connection()
    if connection is None:
        print("Save product terminated")  # Test case
        return {"ok":False,"code":"DB_ERROR","message":"Connection To DataBase Failed!"}

    cursor = connection.cursor()
    queries.insert_product(cursor,name,category,price,quantity)

    cursor.close()
    connection.commit()
    connection.close()

    return {"ok": True, "code": "Success", "message": "Product Successfully Added!"}

def fetch_products():
    connection = config.get_db_connection()
    if connection is None:
        print("Db connection Failed") # Test Case , there is no need to show error, just leave the table empty!
        return

    cursor = connection.cursor()
    products = queries.get_all_products(cursor) # if there is no products then this will return empty list () , otherwise records of products as a list of tuples !
    if not products:
        print("There is no product!") # Test Case !
        return
    return products

def search_product(product_name):
    connection = config.get_db_connection()
    if connection is None:
        print("Database connection failed !") # Test Case
        return
    cursor = connection.cursor()
    product = queries.get_product_by_name(cursor,product_name)
    if product is None:
        print("Product Not Found!")
        return # None

    return product

def save_product(entries): # Entries will be passed out as a dictionary !
    # Extract the dictionary data:
    name = entries['name'].get().strip()
    category = entries['category'].get().strip()
    price = entries['price'].get().strip()
    quantity = entries['quantity'].get().strip()

    # Check if any field is left empty then exit !
    for val in entries.values():
        if val.get().strip() == "":
            print("Some Field was left empty!") # Test Case
            return {"ok":False,"code":"VALIDATION_ERROR","message":"Some Field was left empty!"}

    # Check if name is greater than 2 else exit
    if len(name) < 2:
        print("Too small name") # Test Case
        return {"ok":False,"code":"VALIDATION_ERROR","message":"Name Length Is Too Small!"}
    # price and quantity must be float and int , and if user enters some other data then show error:
    try:
        price = float(price)
        quantity = int(quantity)
    except:
        print("Price must be a number!") # Test Case
        print("Quantity must be a number") # Test Case
        return {"ok":False,"code":"VALIDATION_ERROR","message":"Price or Quantity Must Be A Number!"}

    # Checking if product already exist , if yes then exit !
    exsisting = find_product_by_name(name) # Return true if product already exist !
    if exsisting:
        print("Product already exist") # Test Case
        return {"ok":False,"code":"ALREADY_EXSISTS","message":"Product Already EXISTS!"} # There can be another scenario where db connection fails so we have to check it out!

    # Just add the product , becasue reaching here means all validation are done!
    return add_product(name,category,price,quantity)
