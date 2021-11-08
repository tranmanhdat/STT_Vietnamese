from os import curdir
import sqlite3

conn = sqlite3.connect("database.db") 
c= conn.cursor()

c.execute("update questionsLib set content='Học viện là nhà trường có uy tín cao, là địa chỉ hợp tác, đầu tư tin cậy của các cơ quan đào tạo' where id=7")
c.execute("select * from questionsLib")
for i in c.fetchall():
    print(i)

conn.commit()
conn.close()