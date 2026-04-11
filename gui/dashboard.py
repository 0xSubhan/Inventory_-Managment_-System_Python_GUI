import tkinter as tk
import tkinter.ttk as ttk
from utility import clear_window
from modules import dashboard_service
from tkinter import messagebox



def show_total_products():
    number_of_products = dashboard_service.fetch_number_of_products()
    if number_of_products["ok"]:
        return number_of_products["result"]
    elif number_of_products["code"] == "DB_FAILED":
        messagebox.showwarning("Warning","Connection to DB failed!")
        return
    else:
        return number_of_products["result"]

def show_total_stock():
    total_stocks = dashboard_service.fetch_total_stocks()
    if total_stocks["ok"]:
        return total_stocks["result"]
    elif total_stocks["code"] == "DB_FAILED":
        messagebox.showwarning("Warning",total_stocks["message"])
        return
    else:
        return total_stocks["result"]

def show_low_stock_items_count():
    low_stock_count = dashboard_service.fetch_low_stock_count()

    if low_stock_count["ok"]:
        return low_stock_count["result"]
    elif low_stock_count["code"] == "DB_FAILED":
        messagebox.showwarning("Warning",low_stock_count["message"])
        return
    else:
        return low_stock_count["result"]

def show_total_revenue():
    total_revenue = dashboard_service.fetch_total_revenue()

    if total_revenue["ok"]:
        return total_revenue["result"]
    elif total_revenue["code"] == "DB_FAILED":
        messagebox.showwarning("Warning",total_revenue["message"])
        return
    else:
        return total_revenue["result"]

def empty_sales_table(sales_table):
    for row in sales_table.get_children():
        sales_table.delete(row)

def update_recent_sales_table(sales_table):
    empty_sales_table(sales_table)

    recent_sales = dashboard_service.fetch_recent_sales()
    print(recent_sales)
    if recent_sales["ok"]:
        for recent_sale in recent_sales["result"]:
            sales_table.insert("","end",values=recent_sale)
    elif recent_sales["code"] == "DB_FAILED":
        messagebox.showwarning("Warning", recent_sales["message"])
        return
    else:
        return


def dashboard_page(window):
    clear_window.clear_main(window)
    window.configure(bg="white")

    page = tk.Frame(window, bg="white")
    page.pack(fill="both", expand=True)

    page.grid_columnconfigure(0, weight=1)

    # Dashboard title
    title = tk.Label(
        page,
        text="DASHBOARD",
        font=("Arial", 24, "bold"),
        bg="white",
        pady=16,
    )
    title.grid(row=0, column=0, sticky="ew")

    ttk.Separator(page, orient="horizontal").grid(row=1, column=0, sticky="ew", padx=20)

    # Top metric cards
    cards_frame = tk.Frame(page, bg="white")
    cards_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=16)

    cards_frame.grid_columnconfigure(0, weight=1)
    cards_frame.grid_columnconfigure(1, weight=1)

    cards = [
        ("Total Products", str(show_total_products())),
        ("Total Stock", str(show_total_stock())),
        ("Low Stock Items", str(show_low_stock_items_count())+" !"),
        ("Total Revenue", str(show_total_revenue())+" RS"),
    ]

    for index, (label_text, value_text) in enumerate(cards):
        row = index // 2
        col = index % 2

        card = tk.Frame(cards_frame, bg="#f5f7fa", bd=1, relief="ridge")
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        tk.Label(
            card,
            text=label_text,
            font=("Arial", 12, "bold"),
            bg="#f5f7fa",
            pady=10,
        ).pack(fill="x")

        tk.Label(
            card,
            text=value_text,
            font=("Arial", 16, "bold"),
            bg="#f5f7fa",
            pady=12,
        ).pack(fill="x")

    # Recent sales section
    recent_sales_title = tk.Label(
        page,
        text="Recent Sales",
        font=("Arial", 14, "bold"),
        bg="white",
        pady=8,
    )
    recent_sales_title.grid(row=3, column=0, sticky="ew")

    ttk.Separator(page, orient="horizontal").grid(row=4, column=0, sticky="ew", padx=20)

    table_frame = tk.Frame(page, bg="white")
    table_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=(10, 20))

    columns = ("date", "product", "qty", "total")
    sales_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)

    sales_table.heading("date", text="Date")
    sales_table.heading("product", text="Product")
    sales_table.heading("qty", text="Qty")
    sales_table.heading("total", text="Total")

    sales_table.column("date", width=150, anchor="center")
    sales_table.column("product", width=220, anchor="center")
    sales_table.column("qty", width=100, anchor="center")
    sales_table.column("total", width=150, anchor="center")

    sales_table.insert("", "end", values=("...", "...", "...", "..."))
    sales_table.pack(fill="both", expand=True)

    page.grid_rowconfigure(5, weight=1)

    update_recent_sales_table(sales_table)
