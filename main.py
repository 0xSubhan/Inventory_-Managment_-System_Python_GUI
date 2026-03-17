import tkinter as tk
from gui import dashboard
from gui import product
from gui import report
from gui import sale
from gui import stock

# Root Window
root = tk.Tk()
root.geometry('1920x1080')
root.title("Inventory Managment System")
root.minsize(900, 600)

# SideBar Window Frame
side_frame = tk.Frame(root, bg="lightgray")
side_frame.pack(side="left", fill="y")  # fill vertical space
# Force sidebar width
side_frame.config(width=200)
side_frame.pack_propagate(False)  # prevent shrinking to fit content

# Main Window Frame
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side="right", fill="both", expand=True)  # take remaining space
# Interface

def exit_inventory():
    root.destroy()

def show_page(this_page):
    # Display the provided page
    this_page(main_frame)

# SideBar Window Frame : Configure
dashboard_btn = tk.Button(side_frame,text="DashBoard",pady=10,command=lambda : show_page(dashboard.dashboard_page),font=("Arial", 15, "bold")) # argument is a function pointer/Reference Not a call!
dashboard_btn.pack(fill="x",padx=12,pady=20)

product_btn = tk.Button(side_frame,text="Products",pady=10,command=lambda : show_page(product.product_page),font=("Arial", 15, "bold"))
product_btn.pack(fill="x",padx=12,pady=20)

stock_btn = tk.Button(side_frame,text="Stocks",pady=10,command=lambda : show_page(stock.stock_page),font=("Arial", 15, "bold"))
stock_btn.pack(fill="x",padx=12,pady=20)

sale_btn = tk.Button(side_frame,text="Sales",pady=10,command=lambda : show_page(sale.sale_page),font=("Arial", 15, "bold"))
sale_btn.pack(fill="x",padx=12,pady=20)

report_btn = tk.Button(side_frame,text="Reports",pady=10,command=lambda : show_page(report.report_page),font=("Arial", 15, "bold"))
report_btn.pack(fill="x",padx=12,pady=20)

exit_btn = tk.Button(side_frame,text="Exit",pady=10,command=exit_inventory,font=("Arial", 15, "bold"))
exit_btn.pack(fill="x",padx=12,pady=20)

# Main window Frame : Configure // Default to Dashboard
dashboard.dashboard_page(main_frame)










# Main Loop
root.mainloop()