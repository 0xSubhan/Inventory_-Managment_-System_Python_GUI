import tkinter as tk
from tkinter import messagebox, ttk

from gui.product import clear_search_field
from utility import clear_window
from gui import product
from modules import stock_service

def handle_stock_upgrade(entries,stock_table):
    result = stock_service.upgrade_stock(entries)

    if result['ok']:
        messagebox.showinfo("Success",result["message"],default='ok')
        refresh_stock_table(stock_table)
        product.clear_form(entries)
    elif result['code'] == "VALIDATION_ERROR":
        messagebox.showwarning("Warning",result["message"],default='ok')
        product.clear_form(entries)

def empty_stock_table(stock_table):
    for row in stock_table.get_children():
        stock_table.delete(row)


def refresh_stock_table(stock_table):
    empty_stock_table(stock_table)

    products = stock_service.fetch_products_with_stocklvl(threshold=10)

    for product in products:
        print(product)
        stock_table.insert("","end",values=product)

def show_stock_search_result(product_record,stock_table,threshold):
    empty_stock_table(stock_table)


    productid, name, category, price, quantity, _ = product_record
    stock_lvl = "HIGH" if quantity >= threshold else "LOW"

    stock_table.insert("","end",values=(productid,name,category,price,quantity,stock_lvl))


def handle_stock_search(entry_obj,stock_table,threshold=10):
    product_name = entry_obj.get().strip().lower()
    product_record = stock_service.fetch_product(product_name)
    print(product_record)
    if product_record:
        show_stock_search_result(product_record,stock_table,threshold)
        clear_search_field(entry_obj)
    else:
        messagebox.showwarning("Search","No Record Found")
        clear_search_field(entry_obj)
        refresh_stock_table(stock_table)


def stock_page(window):
    clear_window.clear_main(window)
    window.configure(bg="#f4f6fb")

    header = tk.Frame(window, bg="#1f2a44", height=80)
    header.pack(fill="x")
    header.pack_propagate(False)

    title = tk.Label(
        header,
        text="Stock Managment",
        bg="#1f2a44",
        fg="white",
        font=("Helvetica", 22, "bold"),
    )
    title.pack(side="left", padx=24)

    content = tk.Frame(window, bg="#f4f6fb", padx=24, pady=20)
    content.pack(fill="both", expand=True)

    search_card = tk.Frame(content, bg="white", padx=16, pady=14, bd=1, relief="solid")
    search_card.pack(fill="x", pady=(0, 14))

    search_label = tk.Label(
        search_card,
        text="Search Product",
        bg="white",
        fg="#1f2a44",
        font=("Helvetica", 12, "bold"),
    )
    search_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

    search_entry = tk.Entry(search_card, font=("Helvetica", 11), width=40)
    search_entry.grid(row=1, column=0, padx=(0, 10), sticky="ew",ipady=5)

    search_btn = tk.Button(
        search_card,
        text="Search",
        bg="#2f6fed",
        fg="white",
        relief="flat",
        padx=16,
        command=lambda: handle_stock_search(search_entry,stock_table),
    )
    search_btn.grid(row=1, column=1, sticky="w")
    search_card.grid_columnconfigure(0, weight=1)

    refresh_btn = tk.Button(
        search_card,
        text="Refresh Table",
        bg="#2f6fed",
        fg="white",
        relief="flat",
        padx=16,
        command=lambda: refresh_stock_table(stock_table),
    )
    refresh_btn.grid(row=1, column=2, sticky="w")
    refresh_btn.grid_columnconfigure(0, weight=1)

    body = tk.Frame(content, bg="#f4f6fb")
    body.pack(fill="both", expand=True)

    form_card = tk.Frame(body, bg="white", padx=16, pady=16, bd=1, relief="solid")
    form_card.pack(side="left", fill="y", padx=(0, 12))

    form_title = tk.Label(
        form_card,
        text="Add / Update Product",
        bg="white",
        fg="#1f2a44",
        font=("Helvetica", 12, "bold"),
    )
    form_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

    fields = [
        ("name", "Product Name"),
        ("stock", "Add Quantity")

    ]
    entries = {}
    # Didnt get the logic of This ??
    for row, (key, text) in enumerate(fields, start=1):
        tk.Label(form_card, text=text, bg="white", anchor="w").grid(row=row, column=0, sticky="w", pady=6)
        entry = tk.Entry(form_card, width=30)
        entry.grid(row=row, column=1, pady=6, padx=(10, 0), sticky="ew")
        entries[key] = entry

    button_row = tk.Frame(form_card, bg="white")
    button_row.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(14, 0), sticky="w")

    tk.Button(
        button_row,
        text="Restock",
        bg="#2f6fed",
        fg="white",
        relief="flat",
        padx=14,
        command=lambda: handle_stock_upgrade(entries,stock_table),
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_row,
        text="Clear",
        bg="#e9edf7",
        fg="#1f2a44",
        relief="flat",
        padx=14,
        command=lambda: product.clear_form(entries),
    ).pack(side="left")

    form_card.grid_columnconfigure(1, weight=1)

    # Show table UI :
    table_card = tk.Frame(body, bg="white", padx=16, pady=16, bd=1, relief="solid")
    table_card.pack(side="left", fill="both", expand=True)

    tk.Label(
        table_card,
        text="Products",
        bg="white",
        fg="#1f2a44",
        font=("Helvetica", 12, "bold"),
    ).pack(anchor="w", pady=(0, 10))

    table_container = tk.Frame(table_card, bg="white")
    table_container.pack(fill="both", expand=True)

    columns = ("id","name", "category", "price", "stock","stocklvl")
    stock_table = ttk.Treeview(table_container, columns=columns, show="headings")

    stock_table.heading("id", text="ID")
    stock_table.heading("name", text="Name")
    stock_table.heading("category", text="Category")
    stock_table.heading("price", text="Price")
    stock_table.heading("stock", text="Stock")
    stock_table.heading("stocklvl", text="Stock Level")

    stock_table.column("id", width=100, anchor="w")
    stock_table.column("name", width=180, anchor="w")
    stock_table.column("category", width=140, anchor="w")
    stock_table.column("price", width=100, anchor="center")
    stock_table.column("stock", width=100, anchor="center")
    stock_table.column("stocklvl", width=100, anchor="center")

    y_scroll = ttk.Scrollbar(table_container, orient="vertical", command=stock_table.yview)
    stock_table.configure(yscrollcommand=y_scroll.set)

    stock_table.pack(side="left", fill="both", expand=True)
    y_scroll.pack(side="right", fill="y")

    refresh_stock_table(stock_table) # Initial Table View !
