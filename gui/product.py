import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, ttk
from modules import product_service
from utility import clear_window

def clear_form(entries): # entries are passed in as dictionary !

    for val in entries.values(): # values() will return view to all the value from the dictionary!
        val.delete(0,tk.END)

def refresh_table(product_table):
    # First Deleting Exsisting records:
    empty_product_table(product_table)

    products = product_service.fetch_products()
    for product in products:
        product_table.insert("","end",values=product)


def handle_save(entries,product_table):
    result = product_service.save_product(entries)

    if result["ok"]:
        messagebox.showinfo("Success",result["message"],default='ok')
        clear_form(entries)
        refresh_table(product_table)
    elif result["code"]  in ("VALIDATION_ERROR","DB_ERROR","ALREADY_EXSISTS"):
        messagebox.showwarning("Warning",result["message"],default='ok')
        clear_form(entries)
    else:
        messagebox.showerror("Error",result["message"],default='ok')
        clear_form(entries)

def show_search_result(product_table,record):
    # First Deleting Exsisting records:
    empty_product_table(product_table)
    product_table.insert("","end",values=record)

def clear_search_field(search_entry_object):
    search_entry_object.delete(0,tk.END)

def empty_product_table(product_table):
    for rows in product_table.get_children():
        product_table.delete(rows)


def handle_search(product_entry,product_table):
    product = product_entry.get().strip().lower() # get the name as a string !
    product_record = product_service.search_product(product)
    if product_record:
        print("Record Found") # later show in message box!
        show_search_result(product_table,product_record)
        clear_search_field(product_entry)
    else:
        # That means search returned None so we will empty the table with popup "no record" !
        messagebox.showwarning("Search","No Record Found !")
        refresh_table(product_table)
########################################################################################################################
def product_page(window):
    clear_window.clear_main(window)
    window.configure(bg="#f4f6fb")

    header = tk.Frame(window, bg="#1f2a44", height=80)
    header.pack(fill="x")
    header.pack_propagate(False)

    title = tk.Label(
        header,
        text="Product Management",
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
        command=lambda: handle_search(search_entry,product_table),
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
        command=lambda: refresh_table(product_table),
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
        ("category", "Category"),
        ("price", "Price"),
        ("quantity", "Quantity"),
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
        text="Save",
        bg="#2f6fed",
        fg="white",
        relief="flat",
        padx=14,
        command=lambda: handle_save(entries,product_table),
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_row,
        text="Clear",
        bg="#e9edf7",
        fg="#1f2a44",
        relief="flat",
        padx=14,
        command=lambda: clear_form(entries),
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

    columns = ("id","name", "category", "price", "quantity","status")
    product_table = ttk.Treeview(table_container, columns=columns, show="headings")

    product_table.heading("id", text="ID")
    product_table.heading("name", text="Name")
    product_table.heading("category", text="Category")
    product_table.heading("price", text="Price")
    product_table.heading("quantity", text="Quantity")
    product_table.heading("status", text="Status")


    product_table.column("id", width=100, anchor="w")
    product_table.column("name", width=180, anchor="w")
    product_table.column("category", width=140, anchor="w")
    product_table.column("price", width=100, anchor="center")
    product_table.column("quantity", width=100, anchor="center")
    product_table.column("status", width=100, anchor="center")


    y_scroll = ttk.Scrollbar(table_container, orient="vertical", command=product_table.yview)
    product_table.configure(yscrollcommand=y_scroll.set)

    product_table.pack(side="left", fill="both", expand=True)
    y_scroll.pack(side="right", fill="y")

    refresh_table(product_table) # Initial Table view !
