import sqlite3
from flask import current_app,g
conn = sqlite3.connect('database.db')
print ("Opened database successfully")
# conn.execute('drop table collection')
#conn.execute('delete from collection')
#conn.execute('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL,author INT DEFAULT 1)')
#conn.execute('CREATE TABLE collection (id INTEGER PRIMARY KEY AUTOINCREMENT,id_user int,tittle TEXT,topic TEXT, content TEXT)')

# cur.execute("SELECT *  FROM collection order by id desc limit 1")
print ("Table created successfully")
conn.close()