c.execute("select * from testCodes")
for item in c.fetchall():
    print(item)