import sqlite3

class Database:
    def __init__(self, db, table_name):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        self.create_table()
    

    def create_table(self):
        # Tạo bảng nếu chưa tồn tại
        if self.table_name == 'expense_record':
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS expense_record (
                    category_ex TEXT,
                    name_ex TEXT,
                    price_ex INT,
                    date_ex TEXT
                )
            ''')
        elif self.table_name == 'income_record':
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS income_record (
                    category_in TEXT,
                    name_in TEXT,
                    price_in INT,
                    date_in TEXT
                )
            ''')
        self.conn.commit()

    def insert_ex(self, category_ex, name_ex, price_ex, date_ex):
        # Thêm bản ghi mới vào bảng
        query = f'INSERT INTO {self.table_name} (category_ex, name_ex, price_ex, date_ex) VALUES (?, ?, ?, ?)'
        self.cursor.execute(query, (category_ex, name_ex, price_ex, date_ex))
        self.conn.commit()
        
    def insert_in(self, category_in, name_in, price_in, date_in):
        # Thêm bản ghi mới vào bảng
        query = f'INSERT INTO {self.table_name} (category_in, name_in, price_in, date_in) VALUES (?, ?, ?, ?)'
        self.cursor.execute(query, (category_in, name_in, price_in, date_in))
        self.conn.commit()

    def fetch_ex(self):
        self.cursor.execute("SELECT * FROM expense_record")
        return self.cursor.fetchall()

    def fetch_in(self):
        self.cursor.execute("SELECT * FROM income_record")
        return self.cursor.fetchall()

    def update_ex(self, rowid, category_ex, name_ex, price_ex, date_ex):
        # Cập nhật bản ghi dựa trên rowid
        query = f'UPDATE {self.table_name} SET category_ex=?, name_ex=?, price_ex=?, date_ex=? WHERE rowid=?'
        self.cursor.execute(query, (category_ex, name_ex, price_ex, date_ex, rowid))
        self.conn.commit()
        
    def update_in(self, rowid, category_in, name_in, price_in, date_in):
        # Cập nhật bản ghi dựa trên rowid
        query = f'UPDATE {self.table_name} SET category_in=?, name_in=?, price_in=?, date_in=? WHERE rowid=?'
        self.cursor.execute(query, (category_in, name_in, price_in, date_in, rowid))
        self.conn.commit()
        
    def remove_ex(self, rowid):
        # Xoá bản ghi dựa trên rowid
        query = f'DELETE FROM {self.table_name} WHERE rowid=?'
        self.cursor.execute(query, (rowid,))
        self.conn.commit()
        
    def remove_in(self, rowid):
        # Xoá bản ghi dựa trên rowid
        query = f'DELETE FROM {self.table_name} WHERE rowid=?'
        self.cursor.execute(query, (rowid,))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()