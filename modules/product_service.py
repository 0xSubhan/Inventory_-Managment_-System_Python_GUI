import tkinter as tk
from database import queries
from database import config
from database.queries import get_product_by_name


def find_product_by_name(name):
    connection = config.get_db_connection()
    if connection is None:
        print("Save product terminated")  # Test case
        return

    cursor = connection.cursor()
    product = get_product_by_name(cursor,name)

    cursor.close()
    connection.close()
    return product

def add_product(name,category,price,quantity):
    connection = config.get_db_connection()
    if connection is None:
        print("Save product terminated")  # Test case
        return

    cursor = connection.cursor()
    queries.insert_product(cursor,name,category,price,quantity)


    cursor.close()
    connection.commit()
    connection.close()


def save_product(entries):

    # Entries will be passed out as a dictionary !
    # Extract the dictionary data:
    name = entries['name'].get().strip()
    category = entries['category'].get().strip()
    price = entries['price'].get().strip()
    quantity = entries['quantity'].get().strip()

    # Check if any field is left empty then exit !
    for val in entries.values():
        if val.get().strip() == "":
            print("Some Field was left empty!") # Test Case
            return

    # Check if name is greater than 2 else exit
    if len(name) < 2:
        print("Too small name") # Test Case
        return
    # price and quantity must be float and int , and if user enters some other data then show error:
    try:
        price = float(price)
        quantity = int(quantity)
    except:
        print("Price must be a number!") # Test Case
        print("Quantity must be a number") # Test Case
        return

    # Checking if product already exist , if yes then exit !
    exsisting = find_product_by_name(name) # Return true if product already exist !
    if exsisting:
        print("Product already exist") # Test Case
        return

    # Just add the product , becasue reaching here means all validation are done!
    add_product(name,category,price,quantity)

