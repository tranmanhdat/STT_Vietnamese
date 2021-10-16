import sqlite3

conn = sqlite3.connect("database.db") 
c = conn.cursor()

c.execute("update studentTest_Rela set mark=0 where studentId >= 0 ")
c.execute("select * from studentTest_Rela")
print(c.fetchall())
conn.commit()
conn.close()