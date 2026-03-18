import tkinter as tk
from database import queries

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




    queries.insert_product(entries['name'].get().strip(),entries['category'].get().strip(),entries['price'].get().strip(),entries['quantity'].get().strip())