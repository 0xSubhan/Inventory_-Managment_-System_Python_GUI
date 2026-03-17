import tkinter as tk
from utility import clear_window

def sale_page(window):
    clear_window.clear_main(window)
    label = tk.Label(window,text="Sales")
    label.pack()