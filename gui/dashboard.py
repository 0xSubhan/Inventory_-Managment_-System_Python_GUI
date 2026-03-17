import tkinter as tk
from utility import clear_window

def dashboard_page(window):
    clear_window.clear_main(window)
    label = tk.Label(window,text="Dashboard",font=("Arial", 24, "bold"),bg="white",padx=20,pady=20)
    label.grid(row=0,column=0)
    # Tells the first column to expand horizontally.
    window.grid_columnconfigure(0,weight=1)
