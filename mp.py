import csv
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
from mydb import *
from tkinter import ttk
import datetime as dt
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Khởi tạo đối tượng database cho expense và income
expense_data = Database(db='finance.db', table_name='expense_record')
income_data = Database(db='finance.db', table_name='income_record')

# Biến toàn cục
count_ex = 0
selected_rowid_ex = 0
count_in = 0 
selected_rowid_in = 0
#######################################                  BACK END                  #################################
# Bảng expensse record
def saveRecord_ex(category, item_name , item_price, purchase_date):
    try:
        price_ex = float(item_price)
        if price_ex < 0:
            raise ValueError("Giá không được âm")  #Giá không âm
        expense_data.insert_ex(category, item_name, price_ex, purchase_date)  #chèn bản ghi chi tiêu
        fetch_records_ex()
        clearEntries_ex()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def setDate_ex():
    pass
def fetch_records_ex():
    rows = expense_data.fetch_ex()
    for row in tv.get_children(): #Xóa dữ liệu cũ trong treeview
        tv.delete(row)
    for row in rows:    #Thêm dữ liệu mới vào treeview
        tv.insert("", "end", values=row)

def select_record_ex():
    pass
def update_record_ex():
    pass
def refreshData_ex():
    pass
def deleteRow_ex():
    pass
def clearEntries_ex():
    pass

#bảng income record
def saveRecord_in(category, item_name, item_price, purchase_date):
    try:
        price_in = float(item_price)
        if price_in < 0:
            raise ValueError("Giá không được âm")
        income_data.insert_in(category, item_name, price_in, purchase_date)   #chèn bản ghi thu nhập
        fetch_records_in()
        clearEntries_in()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def setDate_in():
    pass
def fetch_records_in():
    rows = income_data.fetch_in()
    for row in zv.get_children():  # Xóa dữ liệu cũ trong treeview
        zv.delete(row)
    for row in rows:  # Thêm dữ liệu mới vào treeview
        zv.insert("", "end", values=row)
def select_record_in():
    pass
def update_record_in():
    pass
def refreshData_in():
    pass
def deleteRow_in():
    pass

# tính totalbalance
def totalBalance():
    pass

################################################## FRONT END #######################################################
ws = Tk()
ws.title('Daily Expenses')
#ws.geometry("2000x2000")
f2 = Frame(ws)
f2.pack() 
expense_label = Label(f2, text="Expense Records 💰                                    Income Records💸 ", font=("Arial", 12, "bold"))
expense_label.pack(side="top")

tv = ttk.Treeview(f2, columns=(1, 2, 3, 4,5), show='headings', height=8)
tv.pack(side = "left", expand=True, fill=BOTH)
tv.column(1, anchor=CENTER, stretch=NO, width=30)
tv.column(2, anchor=CENTER,width=140)
tv.column(3, anchor=CENTER,width=150)
tv.column(4, anchor=CENTER,width=140)
tv.column(5, anchor=CENTER,width=140)
tv.heading(1, text="ID")
tv.heading(2, text="Category") 
tv.heading(3, text="Item Name", )
tv.heading(4, text="Item Price")
tv.heading(5, text="Purchase Date")



zv = ttk.Treeview(f2, columns=(1, 2, 3, 4,5), show='headings', height=8)
zv.pack(side="right")
zv.column(1, anchor=CENTER, stretch=NO, width=30)
zv.column(2, anchor=CENTER,width=140)
zv.column(3, anchor=CENTER,width=150)
zv.column(4, anchor=CENTER,width=140)
zv.column(5, anchor=CENTER,width=140)
zv.heading(1, text="ID")
zv.heading(2, text="Category") 
zv.heading(3, text="Item Name", )
zv.heading(4, text="Item Price")
zv.heading(5, text="Purchase Date")

# Define categories for expenses and incomes
expense_categories = ["Entertaining", "Bills", "Groceries", "Transport", "Healthcare"]
income_categories = ["Salary", "Business", "Investments", "Gifts"]

# Create dropdown for expense categories
frame_expense = LabelFrame(ws, text="Expense Category:", padx=10, pady=10)
frame_expense.pack(fill="x",side="left", padx=10, pady=5)
# Dropdown cho bảng chi tiêu
category_expense = StringVar()
# Dropdown danh mục chi tiêu
Label(frame_expense, text="Danh mục:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
expense_category_dropdown = ttk.Combobox(frame_expense, textvariable=category_expense, values=expense_categories, state="readonly")
expense_category_dropdown.grid(row=0, column=1, padx=5, pady=5)
expense_category_dropdown.current(0)

# Create dropdown for income categories
category_income = StringVar()
frame_income = LabelFrame(ws, text="Income Category:", padx=10, pady=10)
frame_income.pack(fill="x",side="right", padx=10, pady=5)
# Dropdown danh mục thu nhập
Label(frame_income, text="Danh mục: ").grid(row=0, column=0, padx=5, pady=5, sticky=E)
income_category_dropdown = ttk.Combobox(frame_income, textvariable=category_income, values=income_categories, state="readonly")
income_category_dropdown.grid(row=0, column=1, padx=5, pady=5)
income_category_dropdown.current(0)


fetch_records_ex()
fetch_records_in()
ws.mainloop()
