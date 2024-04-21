import sqlite3




conn = sqlite3.connect("clcnsignup.db")
print("connected")
conn.execute('''CREATE TABLE clcnSignUp(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             email TEXT NOT NULL,
             phone TEXT NOT NULL,
             hospital TEXT NOT NULL,
             id_number TEXT NOT NULL,
             password TEXT NOT NULL,
             confirm_password TEXT
)''')

conn.close()


