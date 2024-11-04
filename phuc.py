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
def select_record_ex():
    pass
def update_record_ex():
    global selected_rowid_ex
    if selected_rowid_ex == 0:
        messagebox.showwarning("Warning", "No expense record selected!")
        return
    category_ex = category_entry_ex.get()
    name_ex = name_entry_ex.get()
    price_ex = float(price_entry_ex.get())
    date_ex = date_entry_ex.get()
    expense_data.update_ex(selected_rowid_ex, category_ex, name_ex, price_ex, date_ex)
    refreshData_ex()
def refreshData_ex():
    for row in tv.get_children():
        tv.delete(row)
    records = expense_data.fetch_ex()
    for idx, (category_ex, name_ex, price_ex, date_ex) in enumerate(records, start=1):
        tv.insert("", "end", values=(idx, category_ex, name_ex, price_ex, date_ex))
def deleteRow_ex():
    pass
def clearEntries_ex():
    pass

#bảng income record
def saveRecord_in():
    pass
def setDate_in():
    pass
def fetch_records_in():
    pass
def select_record_in():
    pass
def update_record_in():
    global selected_rowid_in
    if selected_rowid_in == 0:
        messagebox.showwarning("Warning", "No income record selected!")
        return
    category_in = category_entry_in.get()
    name_in = name_entry_in.get()
    price_in = float(price_entry_in.get())
    date_in = date_entry_in.get()
    income_data.update_in(selected_rowid_in, category_in, name_in, price_in, date_in)
    refreshData_in()
def refreshData_in():
    for row in zv.get_children():
        zv.delete(row)
    records = income_data.fetch_in()
    for idx, (category_in, name_in, price_in, date_in) in enumerate(records, start=1):
        zv.insert("", "end", values=(idx, category_in, name_in, price_in, date_in))
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

price_frame_ex = Frame(ws)
price_frame_ex.pack(side="left", padx=(20, 10), pady=(10, 0))

price_label_ex = Label(price_frame_ex, text="Price")
price_label_ex.pack(side="left", padx=(0, 5))

price_entry_ex = Entry(price_frame_ex, width=20)
price_entry_ex.pack(side="left", padx=(0, 5))

update_button_ex = Button(price_frame_ex, text="Update", command=update_record_ex)
update_button_ex.pack(side="left")


price_frame_in = Frame(ws)
price_frame_in.pack(side="right", padx=(10, 20), pady=(10, 0))

price_label_in = Label(price_frame_in, text="Price")
price_label_in.pack(side="left", padx=(0, 5))

price_entry_in = Entry(price_frame_in, width=20)
price_entry_in.pack(side="left", padx=(0, 5))

update_button_in = Button(price_frame_in, text="Update", command=update_record_in)
update_button_in.pack(side="left")

fetch_records_ex()
fetch_records_in()

ws.mainloop()