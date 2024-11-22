# ========================================================================================================================================================================================
# Init
# ========================================================================================================================================================================================

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from tkinter import * #type: ignore
from customtkinter import * #type: ignore
# from ctk_components import *
import customtkinter as ctk
import tkinter as tk
from mydb import *
from tkinter import ttk
import datetime as dt
import time
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

# Khởi tạo đối tượng database cho expense và income
expense_data = Database(db = 'finance.db', 
                        table_name = 'expense_record')

income_data = Database(db = 'finance.db', 
                       table_name = 'income_record')

# Biến toàn cục
count_ex = 0
selected_rowid_ex = 0
count_in = 0
selected_rowid_in = 0

# ========================================================================================================================================================================================
# Functions
# ========================================================================================================================================================================================

# Hàm xác minh ngày tháng
def validate_datetime(string : str) -> bool:
    month_p = r"\d{1,2}[/](\d{1,2})[/]\d{4}"
    day_p = r"(\d{1,2})[/]\d{1,2}[/]\d{4}"
    year_p = r"\d{1,2}[/]\d{1,2}[/](\d{4})"
    i = 0
    # DD/MM/YYYY
    months = re.findall(month_p, string)
    days = re.findall(day_p, string)
    years = re.findall(year_p, string)
    for m in months:
        m = int(m)
        d = int(days[i])
        y = int(years[i])
        if m <= 12:
            if m in [1, 3, 5, 7, 8, 10, 12] and d in range(1, 32):
                return True
            elif m in [4, 6, 9, 11] and d in range(1, 31):
                return True
            elif m == 2:
                if d in range(1, 29):
                    return True
                elif d == 29:
                    if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
                        return True
                    else:
                        return False
                else:
                    return False                           
            else:
                return False         
        if m > 12:
            return False
        i += 1
    return False

# Hàm format số (thêm dấu ,)
def format_amount(amount: int):
        return f"{amount:,.0f}".replace(",", ",")
    
def parse_amount(amount_str: str) -> int:
    try:
        clean_str = (amount_str).replace(",", "").replace(".", "")
        return int(clean_str)
    except ValueError:
        return 0    

# Hàm lưu bản ghi expense/income
def saveRecord_ex():
    global count_ex
    
    # Hiển thị trên Treeview mà không gọi refresh ngay lập tức
    if category_ex_menu.get() == 'Select Category' or category_ex_menu.get() == '':
        messagebox.showwarning('Warning', 'Please select a category')
    elif item_name_ex.get() == '':
        messagebox.showwarning('Warning', 'Please insert an item')
    elif transaction_date_ex.get() == '' or validate_datetime(transaction_date_ex.get()) == False:
        messagebox.showwarning('Warning', 'Please choose a date')
    elif str(item_amount_ex.get()).isnumeric() == False or [',', '.'] in list(item_amount_ex.get()):
        messagebox.showwarning('Warning', 'Please enter a valid number')
    else:
        # Lưu vào cơ sở dữ liệu
        expense_data.insert_ex(
            category_ex=category_ex_menu.get(),
            name_ex=item_name_ex.get(),
            price_ex=int(item_amount_ex.get()),
            date_ex=transaction_date_ex.get()
        )
        clearEntries_ex()
        update_total_balance()
        update_plot('months')
        update_plot('years')
        update_plot('days')
        refreshData_ex()
def saveRecord_in():
    global count_in
    
    if category_in_menu.get() == 'Select Category' or category_in_menu.get() == '':
        messagebox.showwarning('Warning', 'Please select a category')
    elif item_name_in.get() == '':
        messagebox.showwarning('Warning', 'Please insert an item')
    elif transaction_date_in.get() == '' or validate_datetime(transaction_date_in.get()) == False:
        messagebox.showwarning('Warning', 'Please enter a validated date')
    elif str(item_amount_in.get()).isnumeric() == False or [',', '.'] in list(item_amount_in.get()):
        messagebox.showwarning('Warning', 'Please enter a valid number')
    else:
        income_data.insert_in(
            category_in=category_in_menu.get(),
            name_in=item_name_in.get(),
            price_in=int(item_amount_in.get()),
            date_in=transaction_date_in.get()
        )

        count_in += 1
    
        clearEntries_in()
        update_total_balance()
        update_plot('months')
        update_plot('years')
        update_plot('days')
        refreshData_in()
# Thiết lập ngày hiện tại
def setDate_ex():
    datevarex.set(f'{dt.datetime.now().day}/{dt.datetime.now().month}/{dt.datetime.now().year}')

def setDate_in():
    datevarin.set(f'{dt.datetime.now().day}/{dt.datetime.now().month}/{dt.datetime.now().year}')

# Xóa các trường nhập liệu
def clearEntries_ex():
    category_ex_menu.set('')
    item_name_ex.delete(0, 'end')
    item_amount_ex.delete(0, 'end')
    transaction_date_ex.delete(0, 'end')
    category_ex_menu.set("Select Category")

def clearEntries_in():
    category_in_menu.set('')
    item_name_in.delete(0, 'end')
    item_amount_in.delete(0, 'end')
    transaction_date_in.delete(0, 'end')
    category_in_menu.set("Select Category")

# Lấy các bản ghi từ database
def fetch_records_ex():
    global count_ex
    count_ex = 0
    records = expense_data.fetch_ex()
    for rec in records:
        expense_table.insert(parent='', index= END, iid=count_ex, values=(count_ex+1, rec[0], rec[1], format_amount(rec[2]), rec[3]))
        count_ex += 1

def fetch_records_in():
    global count_in
    count_in = 0
    records = income_data.fetch_in()
    for rec in records:
        income_table.insert(parent='', index= END, iid=count_in, values=(count_in+1, rec[0], rec[1], format_amount(rec[2]), rec[3]))
        count_in += 1

# Chọn bản ghi để cập nhật
def select_record_ex(event):
    global selected_rowid_ex
    selected = expense_table.focus()    
    val = expense_table.item(selected, 'values')
    try:
        selected_rowid_ex = val[0]
        category_ex_menu.set(val[1])
        namevarex.set(val[2])
        amountvarex.set(parse_amount(val[3]))
        d = val[4]
        datevarex.set(str(d))
    except IndexError:
        pass

def select_record_in(event):
    global selected_rowid_in
    selected = income_table.focus()    
    val = income_table.item(selected, 'values')
    try:
        selected_rowid_in = val[0]
        category_in_menu.set(val[1])
        namevarin.set(val[2])
        amountvarin.set(parse_amount(val[3]))
        d = val[4]
        datevarin.set(str(d))
    except IndexError:
        pass

# Cập nhật bản ghi trong database
def update_record_ex():
    global selected_rowid_ex
    selected = expense_table.focus()
    try:
        # Cập nhật cơ sở dữ liệu
        expense_data.update_ex(
            rowid=selected_rowid_ex,
            category_ex=category_ex_menu.get(),
            name_ex=namevarex.get(),
            price_ex=int(amountvarex.get()),
            date_ex=datevarex.get()
        )
        
        # Cập nhật trên Treeview
        expense_table.item(selected, text="", values=(
            selected_rowid_ex,
            category_ex_menu.get(),
            namevarex.get(),
            format_amount(amountvarex.get()),
            datevarex.get()
        ))
        
        update_total_balance()
        update_plot('months')
        update_plot('years')
        update_plot('days')
        clearEntries_ex()
        
    except Exception as ep:
        pass

def update_record_in():
    global selected_rowid_in
    selected = income_table.focus()
    try:
        # Cập nhật cơ sở dữ liệu
        income_data.update_in(
            rowid=selected_rowid_in,
            category_in=category_in_menu.get(),
            name_in=namevarin.get(),
            price_in=int(amountvarin.get()),
            date_in=datevarin.get()
        )
        income_table.delete(selected_rowid_in)
        # Cập nhật trên Treeview
        income_table.item(selected, text="", values=(
            selected_rowid_in,
            category_in_menu.get(),
            namevarin.get(),
            format_amount(amountvarin.get()),
            datevarin.get()
        ))
        
        update_total_balance()
        update_plot('months')
        update_plot('years')
        update_plot('days')
        clearEntries_in()
        
    except Exception as ep:
        pass



# Làm mới dữ liệu trong Treeview
def refreshData_ex():
    # Xóa tất cả bản ghi hiện có trong Treeview
    for item in expense_table.get_children():
        expense_table.delete(item)
    # Lấy lại tất cả các bản ghi từ database
    fetch_records_ex()

def refreshData_in():
    # Xóa tất cả bản ghi hiện có trong Treeview
    for item in income_table.get_children():
        income_table.delete(item)
    # Lấy lại tất cả các bản ghi từ database
    fetch_records_in()

# Xóa bản ghi đã chọn
def deleteRow_ex():
    global selected_rowid_ex 
    # Kiểm tra xem một hàng có được chọn không
    if selected_rowid_ex:
        # Xóa bản ghi trong database
        expense_data.remove_ex(selected_rowid_ex)
        
        # Xóa bản ghi trong Treeview
        selected = expense_table.selection()  # Lấy mục được chọn
        for item in selected:
            expense_table.delete(item)
        
        # Đặt lại `selected_rowid_ex`
        selected_rowid_ex = 0
        
        
    else:
        messagebox.showwarning("Warning", "Please select a record to delete.")

    update_total_balance()
    update_plot('months')
    update_plot('years')
    update_plot('days')

def deleteRow_in():
    global selected_rowid_in
    # Kiểm tra xem một hàng có được chọn không
    if selected_rowid_in:
        # Xóa bản ghi trong database
        income_data.remove_in(selected_rowid_in)
        
        # Xóa bản ghi trong Treeview
        selected = income_table.selection()  # Lấy mục được chọn
        for item in selected:
            income_table.delete(item)
        
        # Đặt lại `selected_rowid_ex`
        selected_rowid_in = 0
        
        
    else:
        messagebox.showwarning("Warning", "Please select a record to delete.")
    clearEntries_in()
    update_total_balance()
    update_plot('months')
    update_plot('years')
    update_plot('days')

# Tạo Treeview với config mặc định là expand = True và fill = BOTH
def create_treeview(frame, columns):
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text = col)
        tree.column(col, width = 100)
    tree.pack(expand = True, fill = BOTH)
    return tree

# Hàm ngắt chương trình
def close_program():  
    root.quit()

    
# Cập nhật tổng thu/chi
def update_total_balance():
    # Tính toán balance từ các bản ghi
    total_expense_records = expense_data.fetch_ex()
    total_income_records = income_data.fetch_in()

    total_expense = sum([int(record[2]) for record in total_expense_records if record[2]])
    total_income = sum([int(record[2]) for record in total_income_records if record[2]])

    # Cập nhật giá trị balance
    balance = total_income - total_expense
    res = format_amount(balance)
    total_balance_label.configure(text = f"{res} đ ")

# Phục hồi record 
def retrive_records():
    fetch_records_ex()
    fetch_records_in()
    
def totalBalance():
    # Lấy tổng các bản ghi chi tiêu và thu nhập
    total_expense = expense_data.fetch_ex()
    total_income = income_data.fetch_in()
    
    # Tính tổng chi tiêu
    total_expense_sum = sum([(record[2]) for record in total_expense if record[2] not in [None, '']])
    # Tính tổng thu nhập
    total_income_sum = sum([(record[2]) for record in total_income if record[2] not in [None, '']])

    # Tính số dư còn lại
    balance_remaining = total_income_sum - total_expense_sum

    # Kiểm tra nếu số dư âm
    if balance_remaining < 0:
        messagebox.showwarning("Warning", f"You have overspent! 😡 TRY TO SPEND LESS!\nBalance Remaining: {format_amount(balance_remaining)} đ")
    else:
        messagebox.showinfo("Current Balance", f"Total Expense: {format_amount(total_expense_sum)}đ\nTotal Income: {format_amount(total_income_sum)}đ\nBalance Remaining: {format_amount(balance_remaining)}đ")
# ========================================================================================================================================================================================
# Create tab control
# ========================================================================================================================================================================================

root = CTk()
root.title("Expense Tracker") 
root.geometry('1280x720')
root.state('zoomed')
root.resizable(width=True, height=True)

# Tắt cửa sổ sẽ đồng thời dừng chương trình
root.protocol("WM_DELETE_WINDOW", close_program)

tabControl = CTkTabview(root,
                        segmented_button_fg_color='grey',
                        anchor = NW,
                        )
tabControl._segmented_button.grid(sticky="W")
  
main_tab = tabControl.add('Dashboard') 
plot_tab = tabControl.add('Summary') 

tabControl.pack(expand = 1, fill ="both") 

# ========================================================================================================================================================================================
# Tab Dashboard
# ========================================================================================================================================================================================

# font
f = ('Nirmala UI', 18)

category_ex_menu = StringVar() # Category
namevarex = StringVar() # Name
amountvarex = IntVar() # Amount
datevarex = StringVar() # Date

category_in_menu = StringVar() # Category
namevarin = StringVar() # Name
amountvarin = IntVar() # Amount
datevarin = StringVar() # Date

# Uhhhh frame, frame
top_frame = CTkFrame(main_tab, corner_radius=0)
top_frame.pack(side = TOP, expand=True, fill=BOTH) 

bottom_frame = CTkFrame(main_tab)
bottom_frame.pack(side = BOTTOM, expand=True, fill=BOTH) 

left_frame = CTkFrame(top_frame)
left_frame.pack(side = LEFT, expand=True, fill=BOTH) 

right_frame = CTkFrame(top_frame)
right_frame.pack(side = RIGHT, expand=True, fill=BOTH) 

left_top = CTkFrame(left_frame)
left_top.pack(side = TOP, expand=False, fill=BOTH)

right_top = CTkFrame(right_frame)
right_top.pack(side = TOP, expand=False, fill=BOTH)

refresh_btn = CTkButton(
    left_top,
    text = "",
    image = CTkImage(light_image=Image.open("assets\\icon.png"), size = (10, 10)), 
    command = lambda: [refreshData_ex(), refreshData_in()], 
    fg_color = '#66b3d4', 
    border_color = 'black', 
    border_width = 1,
    height = 10,
    width = 10,
)
refresh_btn.pack(side = LEFT)
# ========================================================================================================================================================================================
# Bảng Expense
# ========================================================================================================================================================================================

# Frame
expense_label = CTkLabel(left_top, text="Expense Records", font=('Nirmala UI', 22
                                                                 , 'bold'), anchor = S)
expense_label.pack(side = TOP, expand=False, anchor = N)

expense_table_frame = Frame(left_frame)
expense_table_frame.pack(side = TOP, expand=True, fill=BOTH, anchor = E)

# Treeview
expense_table = create_treeview(expense_table_frame, columns = (1, 2, 3, 4, 5))
expense_table.pack(side = LEFT)

expense_table.column(1, anchor=CENTER, stretch=NO, width=40)
expense_table.column(2, anchor=CENTER,width=140)
expense_table.column(3, anchor=CENTER,width=150)
expense_table.column(4, anchor=CENTER,width=140)
expense_table.column(5, anchor=CENTER,width=140)
expense_table.heading(1, text="ID")
expense_table.heading(2, text="Category") 
expense_table.heading(3, text="Item Name", )
expense_table.heading(4, text="Item Price")
expense_table.heading(5, text="Purchase Date")

expense_table.bind("<ButtonRelease-1>", select_record_ex)

# Phần bên dưới cái bảng
expense_functions = CTkFrame(left_frame, corner_radius=0)
expense_functions.pack(side = BOTTOM, expand=True, fill=BOTH)

CTkLabel(expense_functions, text='Expense Category', font=f).grid(row=0, column=0, sticky=W)
CTkLabel(expense_functions, text='Item Name', font=f).grid(row=1, column=0, sticky=W)
CTkLabel(expense_functions, text='Price', font=f).grid(row=2, column=0, sticky=W)
CTkLabel(expense_functions, text='Date (DD/MM/YYYY)', font=f).grid(row=3, column=0, sticky=W)

categories_ex = ["Food", 
                 "Groceries", 
                 "Bills", 
                 "Entertainment", 
                 "Clothes", 
                 "Transport",
                 "Healthcare",
                 "Household", 
                 "Others"
                 ]
category_ex_menu = CTkOptionMenu(expense_functions, 
                                 values = categories_ex, 
                                 fg_color = "#66b3d4",
                                 button_color = "#66b3d4",
                                 font = f
                                 )
category_ex_menu.set("Select Category")
category_ex_menu.grid(row=0, column=1, sticky=EW, padx=(10, 0))

item_name_ex = CTkEntry(expense_functions, font=f, textvariable = namevarex)
item_name_ex.grid(row=1, column=1, sticky=EW, padx=(10, 0))

item_amount_ex = CTkEntry(expense_functions, font=f, textvariable = amountvarex)
item_amount_ex.grid(row=2, column=1, sticky=EW, padx=(10, 0))

transaction_date_ex = CTkEntry(expense_functions, font=f, textvariable = datevarex)
transaction_date_ex.grid(row=3, column=1, sticky=EW, padx=(10, 0))

# Nút bấm
submit_btn_ex = CTkButton(
    expense_functions, 
    text = 'Save Record', 
    font = f, 
    command = saveRecord_ex, 
    fg_color = '#66b3d4',
    border_color = 'black',
    border_width = 1
    )
submit_btn_ex.grid(row=0, column=2, sticky=EW, padx=(10, 0))

clr_btn_ex = CTkButton(
    expense_functions, 
    text = 'Clear Entry', 
    font = f, 
    command = clearEntries_ex, 
    fg_color = '#66b3d4',
    border_color = 'black',
    border_width = 1
    )
clr_btn_ex.grid(row=1, column=2, sticky=EW, padx=(10, 0))

update_btn_ex = CTkButton(
    expense_functions, 
    text = 'Update',
    font = f,
    fg_color = '#66b3d4',
    command = update_record_ex,
    border_color = 'black',
    border_width = 1
    )
update_btn_ex.grid(row=2, column=2, sticky=EW, padx=(10, 0))

del_btn_ex = CTkButton(
    expense_functions, 
    text = 'Delete',
    font = f,
    fg_color = '#66b3d4',
    command = deleteRow_ex,
    border_color = 'black',
    border_width = 1
    )
del_btn_ex.grid(row=3, column=2, sticky=EW, padx=(10, 0))

cur_date_ex = CTkButton(
    expense_functions, 
    text = 'Current Date', 
    font = f, 
    fg_color = "#66b3d4", 
    command = setDate_ex,
    width = 150
    )
cur_date_ex.grid(row=4, column=1, sticky=EW, padx=(10, 0))

# ========================================================================================================================================================================================
# Bảng Income
# ========================================================================================================================================================================================

# Frame
income_label = CTkLabel(right_top, text="Income Records", font=('Nirmala UI', 22, 'bold'), anchor=S)
income_label.pack(side = TOP, expand=False, anchor = N)

income_table_frame = Frame(right_frame)
income_table_frame.pack(side = TOP, expand=True, fill=BOTH, anchor = W)

# Treeview
income_table = create_treeview(income_table_frame, columns=(1, 2, 3, 4, 5))
income_table.pack(side = RIGHT)

income_table.column(1, anchor=CENTER, stretch=NO, width=40)
income_table.column(2, anchor=CENTER,width=140)
income_table.column(3, anchor=CENTER,width=150)
income_table.column(4, anchor=CENTER,width=140)
income_table.column(5, anchor=CENTER,width=140)
income_table.heading(1, text="ID")
income_table.heading(2, text="Category") 
income_table.heading(3, text="Item Name", )
income_table.heading(4, text="Item Price")
income_table.heading(5, text="Income Date")

income_table.bind("<ButtonRelease-1>", select_record_in)

# Phần bên dưới cái bảng
income_functions = CTkFrame(right_frame, corner_radius=0)
income_functions.pack(side = BOTTOM, expand=True, fill=BOTH, anchor = S)

CTkLabel(income_functions, text='Income Category', font=f).grid(row=0, column=0, sticky=W)
CTkLabel(income_functions, text='Item Name', font=f).grid(row=1, column=0, sticky=W)
CTkLabel(income_functions, text='Item Amount', font=f).grid(row=2, column=0, sticky=W)
CTkLabel(income_functions, text='Date (DD/MM/YYYY)', font=f).grid(row=3, column=0, sticky=W)

categories_in = ["Salary",
                 "Gift",
                 "Investments",
                 "Savings",
                 "Interest" ,
                 "Others"
                 ]

category_in_menu = CTkOptionMenu(income_functions, 
                                 values = categories_in, 
                                 fg_color = '#b19cd9', 
                                 button_color = '#b19cd9', 
                                 button_hover_color = "#916ed4",
                                 font = f
                                 )
category_in_menu.set("Select Category")
category_in_menu.grid(row=0, column=1, sticky=EW, padx=(10, 0))

item_name_in = CTkEntry(income_functions, font=f, textvariable=namevarin)
item_name_in.grid(row=1, column=1, sticky=EW, padx=(10, 0))

item_amount_in = CTkEntry(income_functions, font=f, textvariable=amountvarin)
item_amount_in.grid(row=2, column=1, sticky=EW, padx=(10, 0))

transaction_date_in = CTkEntry(income_functions, font=f, textvariable=datevarin)
transaction_date_in.grid(row=3, column=1, sticky=EW, padx=(10, 0))

# Nút bấm

submit_btn_in = CTkButton(
    income_functions, 
    text = 'Save Record', 
    font = f, 
    command = saveRecord_in, 
    fg_color = '#b19cd9',
    border_color = 'black',
    border_width = 1
    )
submit_btn_in.grid(row=0, column=2, sticky=EW, padx=(10, 0))

clr_btn_in = CTkButton(
    income_functions, 
    text = 'Clear Entry', 
    font = f, 
    command = clearEntries_in, 
    fg_color = '#b19cd9',
    border_color = 'black',
    border_width = 1
    )
clr_btn_in.grid(row=1, column=2, sticky=EW, padx=(10, 0))

update_btn_in = CTkButton(
    income_functions, 
    text = 'Update',
    font = f,
    fg_color = '#b19cd9',
    command = update_record_in,
    border_color = 'black',
    border_width = 1
    )
update_btn_in.grid(row=2, column=2, sticky=EW, padx=(10, 0))

del_btn_in = CTkButton(
    income_functions, 
    font = f,
    text = 'Delete',
    fg_color = '#b19cd9',
    command = deleteRow_in,
    border_color = 'black',
    border_width = 1
    )
del_btn_in.grid(row=3, column=2, sticky=EW, padx=(10, 0))

cur_date_in = CTkButton(
    income_functions, 
    text = 'Current Date', 
    font=f, 
    fg_color = '#b19cd9', 
    command = setDate_in,
    width = 150,
    )
cur_date_in.grid(row=4, column=1, sticky=EW, padx=(10, 0))

# Total balance
total_frame = CTkFrame(bottom_frame,
                       corner_radius = 0,
                       fg_color = '#dbdbdb',
                       bg_color = '#dbdbdb'                         
                       )

total_frame.pack(side = TOP, expand = True, fill = BOTH, anchor = N)

Total = CTkButton(total_frame, text='Total Balance', font=('Nirmala UI', 18, 'bold'), command=totalBalance)
Total.pack(side = TOP, anchor = N)

total_balance_label = CTkLabel(total_frame, text = "", font=('Nirmala UI', 22, 'bold'), text_color = "blue")
total_balance_label.pack(side = TOP, anchor = N, expand=True)

# Style 
style = ttk.Style()
style.theme_use("clam")
style.map("Treeview")
style.configure("Treeview", rowheight=30)
style.configure("Treeview.Heading", font=('Nirmala UI', 18, 'bold'))
style.configure("Treeview", font=('Nirmala UI', 16), foreground='black', background='white')

# Scrollbar
scrollbar1 = Scrollbar(expense_table_frame, orient='vertical')
scrollbar1.configure(command=expense_table.yview)
scrollbar1.pack(side = RIGHT, fill="y")
expense_table.config(yscrollcommand=scrollbar1.set)

scrollbar2 = Scrollbar(income_table_frame, orient='vertical')
scrollbar2.configure(command=income_table.yview)
scrollbar2.pack(side = LEFT, fill="y")
income_table.config(yscrollcommand=scrollbar2.set)

# ========================================================================================================================================================================================
# Tab 2
# ========================================================================================================================================================================================

# Plot Font 
fplt = {
    'family': 'Nirmala UI',
    'color': 'black',
    'weight': 'normal',
    'size': 18
}
# Frame
plot_frame = CTkFrame(plot_tab, 
                      bg_color= 'light gray',
                      height = 400)
plot_frame.pack(side = TOP, expand=True, fill = BOTH)
plt.style.use('fivethirtyeight')

text_frame = CTkFrame(plot_tab, bg_color= 'light gray')
# Hàm vẽ đồ thị
def plot_summary(period):
    # Lấy data từ file database
    expense_records = expense_data.fetch_ex()
    income_records = income_data.fetch_in()

    expense_dates = [dt.datetime.strptime(record[3], '%d/%m/%Y') for record in expense_records]
    expense_amounts = [record[2] for record in expense_records]

    income_dates = [dt.datetime.strptime(record[3], '%d/%m/%Y') for record in income_records]
    income_amounts = [record[2] for record in income_records]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.subplots_adjust(bottom=0.2)
    
    def spi():
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_color('gray')
        ax.spines['left'].set_color('gray')
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['left'].set_linewidth(0.5)
    if period == 'days':
        try:
            last_date = max(expense_dates + income_dates)
        except:
            last_date = dt.datetime.now().strftime('%d/%m')
            return last_date
        date_list = [(last_date - dt.timedelta(days=i)).strftime('%d/%m') for i in range(6, -1, -1)]
        x = np.arange(7)
        expense_7day_sum = {date: 0 for date in date_list}
        income_7day_sum = {date: 0 for date in date_list}

        # Tính tổng từng ngày
        for date, amount in zip(expense_dates, expense_amounts):
            date_str = date.strftime('%d/%m')
            if date_str in expense_7day_sum:
                expense_7day_sum[date_str] += amount

        for date, amount in zip(income_dates, income_amounts):
            date_str = date.strftime('%d/%m')
            if date_str in income_7day_sum:
                income_7day_sum[date_str] += amount
                
        ax.bar(x+0.1, [expense_7day_sum[date] for date in date_list], color = '#66b3d4', edgecolor = 'blue', label='Expenses', width = 0.2)
        ax.bar(x-0.1, [income_7day_sum[date] for date in date_list], color = '#b19cd9', edgecolor = 'blue', label='Income', width = 0.2)
        plt.xticks(x, date_list)
        ax.set_title('Last 7 Days Summary', fontdict = fplt)
        
        spi()
        
    elif period == 'months':
        current_year = dt.datetime.now().year
        date_list = [f'{month:02d}/{current_year}' for month in range(1, 13)]

        x = np.arange(12)
        expense_12month_sum = {date: 0 for date in date_list}
        income_12month_sum = {date: 0 for date in date_list}

        # Tính tổng của từng tháng
        for date, amount in zip(expense_dates, expense_amounts):
            date_str = date.strftime('%m/%Y')
            if date_str in expense_12month_sum:
                expense_12month_sum[date_str] += amount

        for date, amount in zip(income_dates, income_amounts):
            date_str = date.strftime('%m/%Y')
            if date_str in income_12month_sum:
                income_12month_sum[date_str] += amount

        ax.bar(x+0.1, [expense_12month_sum[date] for date in date_list], color = '#66b3d4', edgecolor='blue', label='Expenses', width=0.2)
        ax.bar(x-0.1, [income_12month_sum[date] for date in date_list], color = '#b19cd9', edgecolor='blue', label='Income', alpha=0.7, width=0.2)

        plt.xticks(x, date_list)
        ax.set_title('Current Year 12 Months Summary', fontdict = fplt)

        spi()
        
    elif period == 'years':
        try:
            last_date = max(expense_dates + income_dates)
        except:
            last_date = dt.datetime.now().year
            return last_date
        date_list = [(last_date - dt.timedelta(days=365.25 * i)).strftime('%Y') for i in range(3, -1, -1)]
        
        x = np.arange(4)
        expense_4year_sum = {date: 0 for date in date_list}
        income_4year_sum = {date: 0 for date in date_list}

        # Tính tổng của từng năm
        for date, amount in zip(expense_dates, expense_amounts):
            date_str = date.strftime('%Y')
            if date_str in expense_4year_sum:
                expense_4year_sum[date_str] += amount

        for date, amount in zip(income_dates, income_amounts):
            date_str = date.strftime('%Y')
            if date_str in income_4year_sum:
                income_4year_sum[date_str] += amount

        ax.bar(x+0.1, [expense_4year_sum[date] for date in date_list], color = '#66b3d4', edgecolor = 'blue', label='Expenses', width = 0.2)
        ax.bar(x-0.1, [income_4year_sum[date] for date in date_list], color= '#b19cd9', edgecolor = 'blue', label='Income', alpha=0.7, width = 0.2)
        plt.xticks(x, date_list)
        ax.set_title('Last 4 Years Summary', fontdict = fplt)
        
        spi()
        
    elif period == 'pie':
        current_month = dt.datetime.now().month
        current_year = dt.datetime.now().year

        expense_records = [record for record in expense_data.fetch_ex() if dt.datetime.strptime(record[3], '%d/%m/%Y').month == current_month and dt.datetime.strptime(record[3], '%d/%m/%Y').year == current_year]
        income_records = [record for record in income_data.fetch_in() if dt.datetime.strptime(record[3], '%d/%m/%Y').month == current_month and dt.datetime.strptime(record[3], '%d/%m/%Y').year == current_year]

        expense_categories = [record[0] for record in expense_records]
        expense_amounts = [record[2] for record in expense_records]

        income_categories = [record[0] for record in income_records]
        income_amounts = [record[2] for record in income_records]

        expense_df = pd.DataFrame({'Category': expense_categories, 'Amount': expense_amounts})
        income_df = pd.DataFrame({'Category': income_categories, 'Amount': income_amounts})

        expense_summary = expense_df.groupby('Category').sum()
        income_summary = income_df.groupby('Category').sum()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        color = ['#6d904f', '#8f4bd6', '#098bcd', '#e5ae38', '#fc4f30', '#8ad64b', '#e7ef50', '#ef50a3', '#810f7c']
        ax1.pie(expense_summary['Amount'], colors = color, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Expense Categories (Current Month)', fontdict = fplt)
        ax1.legend(expense_summary.index, loc = 'upper left')
        
        ax2.pie(income_summary['Amount'], colors = color, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Income Categories (Current Month)', fontdict = fplt)
        ax2.legend(income_summary.index, loc = 'best')
    try:
        ax.legend(loc = 'upper left')
        ax.tick_params(axis='x', rotation=30)
        ax.grid(axis='x', linestyle='--', alpha=0)
        ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    except: 
        pass
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)
    
# Cập nhật giá trị cho đồ thị
def update_plot(period):
    # Xóa đồ thị trước khi hiện cái mới
    for widget in plot_frame.winfo_children():
        widget.destroy()
    plt.close('all')
    plot_frame.pack_propagate(False)
    plot_summary(period)

# Nút bấm
btn_frame = CTkFrame(plot_tab, bg_color = 'light gray')
btn_frame.pack(side = BOTTOM)

btn_days = CTkButton(
    btn_frame, 
    text="Summary by Days", 
    command = lambda: update_plot('days')
    )
btn_days.pack(side = LEFT, padx=5, pady=5)

btn_months = CTkButton(
    btn_frame, 
    text="Summary by Months", 
    command= lambda: update_plot('months')
    )
btn_months.pack(side = LEFT, padx=5, pady=5)

btn_years = CTkButton(
    btn_frame,
    text="Summary by Years", 
    command= lambda: update_plot('years')
    )
btn_years.pack(side = LEFT, padx=5, pady=5)

btn_pie_chart = CTkButton(
    btn_frame, 
    text="Pie Chart", 
    command= lambda: update_plot('pie')
    )
btn_pie_chart.pack(side = LEFT, padx=5, pady=5)

btn_frame.pack(side = TOP, fill=X)

# ctk config 
ctk.set_appearance_mode("light")

# Gọi hàm cập nhật khi ứng dụng khởi chạy
update_total_balance()
retrive_records()
update_plot('days')

# print(expense_data.fetch_ex())
root.mainloop() 