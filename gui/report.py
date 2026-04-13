import tkinter as tk
import tkinter.ttk as ttk
from gui import dashboard
from utility import clear_window


def report_page(window):
    clear_window.clear_main(window)
    window.configure(bg="white")

    page = tk.Frame(window, bg="white", padx=20, pady=16)
    page.pack(fill="both", expand=True)

    page.grid_columnconfigure(0, weight=1)
    page.grid_rowconfigure(4, weight=1)

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
    tk.Entry(filter_frame, width=16).pack(side="left", padx=(6, 16))

    tk.Label(filter_frame, text="To Date:", bg="white", font=("Arial", 11)).pack(side="left")
    tk.Entry(filter_frame, width=16).pack(side="left", padx=(6, 16))

    tk.Button(filter_frame, text="Filter", width=10).pack(side="left")

    # Quick report buttons
    actions_frame = tk.Frame(page, bg="white")
    actions_frame.grid(row=3, column=0, sticky="w", pady=(0, 12))

    tk.Button(actions_frame, text="Sales Report", width=14).pack(side="left", padx=(0, 8))
    tk.Button(actions_frame, text="Low Stock", width=14).pack(side="left", padx=(0, 8))
    tk.Button(actions_frame, text="Top Products", width=14).pack(side="left")

    ttk.Separator(page, orient="horizontal").grid(row=4, column=0, sticky="new")

    # Result table section
    table_section = tk.Frame(page, bg="white")
    table_section.grid(row=4, column=0, sticky="nsew", pady=(10, 10))
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

    columns = ("date", "product", "qty", "price", "total")
    result_table = ttk.Treeview(table_container, columns=columns, show="headings", height=10)

    result_table.heading("date", text="Date")
    result_table.heading("product", text="Product")
    result_table.heading("qty", text="Qty")
    result_table.heading("price", text="Price")
    result_table.heading("total", text="Total")

    result_table.column("date", width=140, anchor="center")
    result_table.column("product", width=220, anchor="center")
    result_table.column("qty", width=90, anchor="center")
    result_table.column("price", width=120, anchor="center")
    result_table.column("total", width=140, anchor="center")

    y_scroll = ttk.Scrollbar(table_container, orient="vertical", command=result_table.yview)
    result_table.configure(yscrollcommand=y_scroll.set)

    result_table.grid(row=0, column=0, sticky="nsew")
    y_scroll.grid(row=0, column=1, sticky="ns")

    result_table.insert("", "end", values=("...", "...", "...", "...", "..."))

    ttk.Separator(page, orient="horizontal").grid(row=5, column=0, sticky="ew", pady=(0, 10))

    # Footer
    tk.Label(
        page,
        text="Total Revenue: " + str(dashboard.show_total_revenue()) + " PKR",
        font=("Arial", 12, "bold"),
        bg="white",
        anchor="w",
    ).grid(row=6, column=0, sticky="ew")
