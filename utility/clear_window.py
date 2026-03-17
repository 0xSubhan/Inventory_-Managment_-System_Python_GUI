import tkinter as tk

def clear_main(window):
    for widget in window.winfo_children():
        widget.destroy()
