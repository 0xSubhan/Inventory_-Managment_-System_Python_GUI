import tkinter as tk
from pydoc import text
from tkinter import messagebox, ttk
from tkinter import ttk 
from modules import sale_service
from utility import clear_window

def clear_sale_fields(productField,quantityField):
    productField.delete(0,tk.END)
    quantityField.delete(0,tk.END)

def empty_sales_table(sales_table):
    for row in sales_table.get_children():
        sales_table.delete(row)

def update_sale_table(sales_table):
    empty_sales_table(sales_table)

    transactions = sale_service.fetch_all_transactions()
    for transaction in transactions:
        sales_table.insert("","end",values=transaction)

def handle_calculate_total(price_label,product_entry,quantity_entry):
    product_name = product_entry.get().strip().lower()
    product_quantity = quantity_entry.get().strip()

    result = sale_service.calculate_total(product_name,product_quantity)
    if result["ok"]:
        price_label.config(text=str(result["result"]))
    else:
        messagebox.showwarning("Warning",result["message"],default="ok")

def handle_sell_stock(sales_table,product_entry,quantity_entry):
    productName = product_entry.get().strip().lower()
    productQuantity = quantity_entry.get().strip()

    result = sale_service.sell_stock(productName,productQuantity)

    if result["ok"]:
        # update table later
        messagebox.showinfo("Success",result["message"])
        update_sale_table(sales_table)
    else:
        messagebox.showwarning("Warning",result["message"])
        update_sale_table(sales_table)


def sale_page(window):
    clear_window.clear_main(window)
    window.configure(bg="#f4f6fb")

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    content = tk.Frame(window, bg="#f4f6fb", padx=24, pady=20)
    content.grid(row=0, column=0, sticky="nsew")
    content.grid_columnconfigure(0, weight=1)
    content.grid_rowconfigure(1, weight=1)

    header = tk.Frame(content, bg="#1f2a44", height=80)
    header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
    header.grid_propagate(False)
    header.grid_columnconfigure(0, weight=1)

    title = tk.Label(
        header,
        text="SALES MANAGEMENT",
        bg="#1f2a44",
        fg="white",
        font=("Helvetica", 22, "bold"),
    )
    title.grid(row=0, column=0, sticky="w", padx=24, pady=20)

    body = tk.Frame(content, bg="#f4f6fb")
    body.grid(row=1, column=0, sticky="nsew")
    body.grid_columnconfigure(1, weight=1)
    body.grid_rowconfigure(0, weight=1)

    form_card = tk.Frame(body, bg="white", padx=16, pady=16, bd=1, relief="solid")
    form_card.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
    form_card.grid_columnconfigure(1, weight=1)

    tk.Label(
        form_card,
        text="Sales Entry",
        bg="white",
        fg="#1f2a44",
        font=("Helvetica", 12, "bold"),
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

    tk.Label(form_card, text="Product Name:", bg="white", anchor="w").grid(
        row=1, column=0, sticky="w", pady=6
    )
    product_entry = tk.Entry(form_card, width=30)
    product_entry.grid(row=1, column=1, sticky="ew", pady=6, padx=(10, 0))

    tk.Label(form_card, text="Quantity:", bg="white", anchor="w").grid(
        row=2, column=0, sticky="w", pady=6
    )
    quantity_entry = tk.Entry(form_card, width=30)
    quantity_entry.grid(row=2, column=1, sticky="ew", pady=6, padx=(10, 0))

    tk.Button(
        form_card,
        text="Calculate Total",
        bg="#2f6fed",
        fg="white",
        relief="flat",
        padx=14,
        command=lambda : handle_calculate_total(price_label,product_entry,quantity_entry)
    ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(14, 10))

    total_row = tk.Frame(form_card, bg="white")
    total_row.grid(row=4, column=0, columnspan=2, sticky="w", pady=(4, 14))
    tk.Label(total_row, text="Total Price:", bg="white", fg="#1f2a44", font=("Helvetica", 11, "bold")).pack(
        side="left"
    )
    price_label = tk.Label(total_row, text="0", bg="white", fg="#1f2a44", font=("Helvetica", 11))
    price_label.pack(side="left", padx=(8, 0))

    tk.Button(
        form_card,
        text="SELL BUTTON",
        bg="#1f9d55",
        fg="white",
        relief="flat",
        padx=18,
        command=lambda : handle_sell_stock(sales_table,product_entry,quantity_entry)
    ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(6, 0))

    table_card = tk.Frame(body, bg="white", padx=16, pady=16, bd=1, relief="solid")
    table_card.grid(row=0, column=1, sticky="nsew")
    table_card.grid_columnconfigure(0, weight=1)
    table_card.grid_rowconfigure(1, weight=1)

    tk.Label(
        table_card,
        text="Sales History Table",
        bg="white",
        fg="#1f2a44",
        font=("Helvetica", 12, "bold"),
    ).grid(row=0, column=0, sticky="w", pady=(0, 10))

    table_container = tk.Frame(table_card, bg="white")
    table_container.grid(row=1, column=0, sticky="nsew")
    table_container.grid_columnconfigure(0, weight=1)
    table_container.grid_rowconfigure(0, weight=1)

    columns = ("saleid","date", "product", "qty", "price", "total")
    sales_table = ttk.Treeview(table_container, columns=columns, show="headings")

    sales_table.heading("saleid", text="SaleID")
    sales_table.heading("date", text="Date")
    sales_table.heading("product", text="Product")
    sales_table.heading("qty", text="Qty")
    sales_table.heading("price", text="Price")
    sales_table.heading("total", text="Total")

    sales_table.column("saleid", width=140, anchor="w")
    sales_table.column("date", width=140, anchor="w")
    sales_table.column("product", width=220, anchor="w")
    sales_table.column("qty", width=80, anchor="center")
    sales_table.column("price", width=100, anchor="center")
    sales_table.column("total", width=120, anchor="center")

    y_scroll = ttk.Scrollbar(table_container, orient="vertical", command=sales_table.yview)
    sales_table.configure(yscrollcommand=y_scroll.set)

    sales_table.grid(row=0, column=0, sticky="nsew")
    y_scroll.grid(row=0, column=1, sticky="ns")

    update_sale_table(sales_table)
