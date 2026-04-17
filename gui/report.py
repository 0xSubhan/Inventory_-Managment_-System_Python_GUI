import tkinter as tk
import tkinter.ttk as ttk
from gui import dashboard
from modules import sale_service
from tkinter import messagebox
from modules import report_service
from utility import clear_window

selected_report_type = "sales"
TABLE_COLUMNS = ("col1", "col2", "col3", "col4", "col5", "col6")
DATE_PLACEHOLDER = "YYYY-MM-DD"

TABLE_LAYOUTS = {
    "sales": [
        ("col1", "Sale ID", 110),
        ("col2", "Date", 170),
        ("col3", "Product", 220),
        ("col4", "Qty", 90),
        ("col5", "Price", 120),
        ("col6", "Total", 140),
    ],
    "lowstock": [
        ("col1", "Product ID", 110),
        ("col2", "Product", 220),
        ("col3", "Category", 160),
        ("col4", "Qty Left", 110),
        ("col5", "Unit Price", 120),
        ("col6", "Stock Level", 120),
    ],
    "topproduct": [
        ("col1", "Rank", 90),
        ("col2", "Product", 220),
        ("col3", "Category", 160),
        ("col4", "Units Sold", 120),
        ("col5", "Revenue", 140),
        ("col6", "Current Stock", 140),
    ],
}

def empty_report_table(report_table):
    for row in report_table.get_children():
        report_table.delete(row)

def configure_table_layout(report_table,layout_type):
    layout = TABLE_LAYOUTS[layout_type]
    for column_id, heading, width in layout:
        report_table.heading(column_id, text=heading)
        report_table.column(column_id, width=width, anchor="center")

def insert_table_rows(result_table,records):
    for record in records:
        row = list(record)
        if len(row) < len(TABLE_COLUMNS):
            row.extend([""] * (len(TABLE_COLUMNS) - len(row)))
        result_table.insert("", "end", values=tuple(row[:len(TABLE_COLUMNS)]))

def add_date_placeholder(entry):
    entry.insert(0, DATE_PLACEHOLDER)
    entry.config(fg="gray")

    def on_focus_in(_event):
        if entry.get() == DATE_PLACEHOLDER:
            entry.delete(0, "end")
            entry.config(fg="black")

    def on_focus_out(_event):
        if entry.get().strip() == "":
            entry.insert(0, DATE_PLACEHOLDER)
            entry.config(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def get_date_value(entry):
    value = entry.get().strip()
    if value == DATE_PLACEHOLDER:
        return ""
    return value

def reset_date_entry(entry):
    entry.delete(0, "end")
    entry.insert(0, DATE_PLACEHOLDER)
    entry.config(fg="gray")

def handle_filter_report(result_table,from_date_entry,to_date_entry):
    from_date = get_date_value(from_date_entry)
    to_date = get_date_value(to_date_entry)

    if selected_report_type == "sales":
        filtered_result = report_service.fetch_sales_records_by_date(from_date,to_date)
    elif selected_report_type == "topproduct":
        filtered_result = report_service.fetch_top_products_by_date(from_date,to_date)
    else:
        messagebox.showwarning("Warning","Date filter is only available for Sales and Top Products reports.")
        return

    if filtered_result["ok"]:
        empty_report_table(result_table)
        insert_table_rows(result_table,filtered_result["result"])
    else:
        messagebox.showwarning("Warning",filtered_result["message"])

def handle_clear_filter(result_table,from_date_entry,to_date_entry,sale_btn,low_stock_btn,top_product_btn,report_buttons):
    reset_date_entry(from_date_entry)
    reset_date_entry(to_date_entry)

    if selected_report_type == "sales":
        handle_sales_report(result_table,sale_btn,report_buttons)
    elif selected_report_type == "lowstock":
        handle_lowstock_report(result_table,low_stock_btn,report_buttons)
    elif selected_report_type == "topproduct":
        handle_top_product_report(result_table,top_product_btn,report_buttons)
    else:
        handle_sales_report(result_table,sale_btn,report_buttons)

def set_active_button(clicked_button,report_buttons):
    for btn in report_buttons:
        btn.config(state="normal")

    clicked_button.config(state="disabled")

def handle_sales_report(result_table,clicked_button,report_buttons):
    # First Empty the table:
    empty_report_table(result_table)

    global selected_report_type
    selected_report_type = "sales"

    configure_table_layout(result_table,selected_report_type)
    set_active_button(clicked_button,report_buttons)

    # Now we need to show all sales report !
    transactions = sale_service.fetch_all_transactions()

    if transactions["ok"]:
        insert_table_rows(result_table,transactions["result"])
    else:
        messagebox.showwarning("Warning","No Sales Record At the moment !")
        return

def handle_lowstock_report(result_table,clicked_button,report_buttons):
    # First Empty the table:
    empty_report_table(result_table)

    global selected_report_type
    selected_report_type = "lowstock"

    configure_table_layout(result_table,selected_report_type)
    set_active_button(clicked_button,report_buttons)

    low_stock_records = report_service.fetch_low_stock_records()

    if low_stock_records["ok"]:
        insert_table_rows(result_table,low_stock_records["result"])
    else:
        messagebox.showwarning("Warning",low_stock_records["message"])
        return


def handle_top_product_report(result_table,clicked_button,report_buttons):
    # First Empty the table:
    empty_report_table(result_table)

    global selected_report_type
    selected_report_type = "topproduct"

    configure_table_layout(result_table,selected_report_type)
    set_active_button(clicked_button,report_buttons)
    top_products = report_service.fetch_top_products()

    if top_products["ok"]:
        insert_table_rows(result_table,top_products["result"])
    else:
        messagebox.showwarning("Warning",top_products["message"])
        return  



def report_page(window):
    clear_window.clear_main(window)
    window.configure(bg="white")

    page = tk.Frame(window, bg="white", padx=20, pady=16)
    page.pack(fill="both", expand=True)

    page.grid_columnconfigure(0, weight=1)
    page.grid_rowconfigure(5, weight=1)

    # Header
    tk.Label(
        page,
        text="REPORTS",
        font=("Arial", 24, "bold"),
        bg="white",
        pady=8,
    ).grid(row=0, column=0, sticky="ew")

    ttk.Separator(page, orient="horizontal").grid(row=1, column=0, sticky="ew", pady=(0, 12))

    # Filter row
    filter_frame = tk.Frame(page, bg="white")
    filter_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

    tk.Label(filter_frame, text="From Date:", bg="white", font=("Arial", 11)).pack(side="left")
    from_date_entry = tk.Entry(filter_frame, width=16)
    from_date_entry.pack(side="left", padx=(6, 16))
    add_date_placeholder(from_date_entry)

    tk.Label(filter_frame, text="To Date:", bg="white", font=("Arial", 11)).pack(side="left")
    to_date_entry = tk.Entry(filter_frame, width=16)
    to_date_entry.pack(side="left", padx=(6, 16))
    add_date_placeholder(to_date_entry)

    tk.Button(
        filter_frame,
        text="Filter",
        width=10,
        command=lambda : handle_filter_report(result_table,from_date_entry,to_date_entry)
    ).pack(side="left")
    tk.Button(
        filter_frame,
        text="Clear",
        width=10,
        command=lambda : handle_clear_filter(
            result_table,
            from_date_entry,
            to_date_entry,
            sale_btn,
            low_stock_btn,
            top_product_btn,
            report_buttons
        )
    ).pack(side="left", padx=(8, 0))

    # Quick report buttons
    actions_frame = tk.Frame(page, bg="white")
    actions_frame.grid(row=3, column=0, sticky="w", pady=(0, 12))

    sale_btn = tk.Button(actions_frame, text="Sales Report", width=14,command=lambda : handle_sales_report(result_table,sale_btn,report_buttons))
    sale_btn.pack(side="left", padx=(0, 8))
    low_stock_btn = tk.Button(actions_frame, text="Low Stock", width=14,command=lambda : handle_lowstock_report(result_table,low_stock_btn,report_buttons))
    low_stock_btn.pack(side="left", padx=(0, 8))
    top_product_btn = tk.Button(actions_frame, text="Top Products", width=14,command=lambda : handle_top_product_report(result_table,top_product_btn,report_buttons))
    top_product_btn.pack(side="left")

    report_buttons = (sale_btn,low_stock_btn,top_product_btn)

    ttk.Separator(page, orient="horizontal").grid(row=4, column=0, sticky="new")

    # Result table section
    table_section = tk.Frame(page, bg="white")
    table_section.grid(row=5, column=0, sticky="nsew", pady=(10, 10))
    table_section.grid_columnconfigure(0, weight=1)
    table_section.grid_rowconfigure(1, weight=1)

    tk.Label(
        table_section,
        text="RESULT TABLE",
        font=("Arial", 13, "bold"),
        bg="white",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))


    table_container = tk.Frame(table_section, bg="white")
    table_container.grid(row=1, column=0, sticky="nsew")
    table_container.grid_columnconfigure(0, weight=1)
    table_container.grid_rowconfigure(0, weight=1)

    result_table = ttk.Treeview(table_container, columns=TABLE_COLUMNS, show="headings", height=10)
    configure_table_layout(result_table,selected_report_type)

    y_scroll = ttk.Scrollbar(table_container, orient="vertical", command=result_table.yview)
    result_table.configure(yscrollcommand=y_scroll.set)

    result_table.grid(row=0, column=0, sticky="nsew")
    y_scroll.grid(row=0, column=1, sticky="ns")

    handle_sales_report(result_table,sale_btn,report_buttons)

    ttk.Separator(page, orient="horizontal").grid(row=6, column=0, sticky="ew", pady=(0, 10))

    # Footer
    tk.Label(
        page,
        text="Total Revenue: " + str(dashboard.show_total_revenue()) + " PKR",
        font=("Arial", 12, "bold"),
        bg="white",
        anchor="w",
    ).grid(row=7, column=0, sticky="ew")
