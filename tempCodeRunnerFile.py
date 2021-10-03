# c.execute('''create table students(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     studentCode TEXT UNIQUE NOT NULL,
#     studentName TEXT NOT NULL,
#     userId INT,
#     classId INT,
#     description TEXT,
#     FOREIGN KEY(studentName) REFERENCES users(username),
#     FOREIGN KEY(userId) REFERENCES users(id),
#     FOREIGN KEY(classId) REFERENCES classes(id) 
# )''')