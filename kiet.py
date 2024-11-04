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
def saveRecord_ex():
    pass
def setDate_ex():
    pass
def fetch_records_ex():
    pass
def select_record_ex(event):
    global selected_rowid_ex
    clearEntries_ex()
    selected_row = tv.focus()
    data = tv.item(selected_row)
    selected_rowid_ex = data['values'][0]
    category_var_ex.set(data['values'][1])
    item_name_var_ex.set(data['values'][2])
    price_var_ex.set(data['values'][3])
    date_var_ex.set(data['values'][4])

def update_record_ex():
    pass
def refreshData_ex():
    pass
def deleteRow_ex():
    pass
def clearEntries_ex():
    category_var_ex.set('')
    item_name_var_ex.set('')
    price_var_ex.set('')
    date_var_ex.set('')

#bảng income record
def saveRecord_in():
    pass
def setDate_in():
    pass
def fetch_records_in():
    pass
def select_record_in(event):
    global selected_rowid_in
    clearEntries_in()
    selected_row = zv.focus()
    data = zv.item(selected_row)
    selected_rowid_in = data['values'][0]
    category_var_in.set(data['values'][1])
    item_name_var_in.set(data['values'][2])
    price_var_in.set(data['values'][3])
    date_var_in.set(data['values'][4])
def update_record_in():
    pass
def refreshData_in():
    pass
def deleteRow_in():
    pass
def clearEntries_in():
    category_var_in.set('')
    item_name_var_in.set('')
    price_var_in.set('')
    date_var_in.set('')

# tính totalbalance
def totalBalance():
    pass

################################################## FRONT END #######################################################
# goc cua file
ws = Tk()
price_var_in = StringVar()
date_var_in = StringVar()
price_var_ex = StringVar()
date_var_ex = StringVar()
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

fetch_records_ex()
fetch_records_in()
# nhiem vu 2
# Expense Treeview
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4, 5), show='headings', height=8)
tv.pack(side="left", expand=True, fill=BOTH)
tv.column(1, anchor=CENTER, stretch=NO, width=30)
tv.column(2, anchor=CENTER, width=140)
tv.column(3, anchor=CENTER, width=150)
tv.column(4, anchor=CENTER, width=140)
tv.column(5, anchor=CENTER, width=140)
tv.heading(1, text="ID")
tv.heading(2, text="Category")
tv.heading(3, text="Item Name")
tv.heading(4, text="Item Price")
tv.heading(5, text="Purchase Date")
tv.bind("<ButtonRelease-1>", select_record_ex)

# Income Treeview
zv = ttk.Treeview(f2, columns=(1, 2, 3, 4, 5), show='headings', height=8)
zv.pack(side="right")
zv.column(1, anchor=CENTER, stretch=NO, width=30)
zv.column(2, anchor=CENTER, width=140)
zv.column(3, anchor=CENTER, width=150)
zv.column(4, anchor=CENTER, width=140)
zv.column(5, anchor=CENTER, width=140)
zv.heading(1, text="ID")
zv.heading(2, text="Category")
zv.heading(3, text="Item Name")
zv.heading(4, text="Item Price")
zv.heading(5, text="Purchase Date")
zv.bind("<ButtonRelease-1>", select_record_in)

# Expense Form
frame_expense_form = Frame(ws)
frame_expense_form.pack(side=LEFT, padx=10, pady=10)

Label(frame_expense_form, text="Category:").grid(row=0, column=0, padx=10, pady=5)
category_var_ex = StringVar()
category_dropdown_ex = ttk.Combobox(frame_expense_form, textvariable=category_var_ex)
category_dropdown_ex['values'] = ('Entertaining', 'Bills', 'Food', 'Transport', 'Others')
category_dropdown_ex.grid(row=0, column=1, padx=10, pady=5)

Label(frame_expense_form, text="Item Name:").grid(row=1, column=0, padx=10, pady=5)
item_name_var_ex = StringVar()
Entry(frame_expense_form, textvariable=item_name_var_ex).grid(row=1, column=1, padx=10, pady=5)

Button(frame_expense_form, text="Save Expense", command=saveRecord_ex).grid(row=2, column=0, padx=10, pady=5)
Button(frame_expense_form, text="Clear Entry", command=clearEntries_ex).grid(row=2, column=1, padx=10, pady=5)

# Income Form
frame_income_form = Frame(ws)
frame_income_form.pack(side=RIGHT, padx=10, pady=10)

Label(frame_income_form, text="Category:").grid(row=0, column=0, padx=10, pady=5)
category_var_in = StringVar()
category_dropdown_in = ttk.Combobox(frame_income_form, textvariable=category_var_in)
category_dropdown_in['values'] = ('Salary', 'Bonus', 'Investment', 'Others')
category_dropdown_in.grid(row=0, column=1, padx=10, pady=5)

Label(frame_income_form, text="Item Name:").grid(row=1, column=0, padx=10, pady=5)
item_name_var_in = StringVar()
Entry(frame_income_form, textvariable=item_name_var_in).grid(row=1, column=1, padx=10, pady=5)

Button(frame_income_form, text="Save Income", command=saveRecord_in).grid(row=2, column=0, padx=10, pady=5)
Button(frame_income_form, text="Clear Entry", command=clearEntries_in).grid(row=2, column=1, padx=10, pady=5)

fetch_records_ex()
fetch_records_in()
ws.mainloop()