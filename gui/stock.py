import tkinter as tk
from utility import clear_window

def stock_page(window):
    clear_window.clear_main(window)
    label = tk.Label(window,text="Stocks")
    label.pack()
