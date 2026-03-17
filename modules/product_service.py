import tkinter as tk
from database import queries

def save_product(entries):
    # Entries will be passed out as a dictionary !
    for val in entries.values():
        if val == None:
            return


    queries.insert_product(entries['name'].get(),entries['category'].get(),entries['price'].get(),entries['quantity'].get())