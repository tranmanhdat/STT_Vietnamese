import sqlite3
from flask import current_app,g
conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON")

# ========== table users =======
c.execute('''create table users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT UNIQUE,
    description TEXT
) ''')
c.execute("insert into users(description) values('học viên')")
c.execute("insert into users(description) values('giảng viên')")
c.execute("select * from users")
print(c.fetchall())

# # # ========== table classes =======
c.execute(''' create table classes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    className TEXT UNIQUE NOT NULL,
    description TEXT
)
''')
c.execute("insert into classes(className) values('Công nghệ thông tin 2')")
c.execute("select * from classes")
print(c.fetchall())

# # # ========== table students =======
c.execute('''create table students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    studentCode TEXT UNIQUE NOT NULL,
    studentName TEXT NOT NULL,
    userId INT,
    classId INT,
    description TEXT,
    FOREIGN KEY(userId) REFERENCES users(id),
    FOREIGN KEY(classId) REFERENCES classes(id) 
)''')

c.execute("insert into students(studentCode, studentName, userId, classId) values('187914407', 'Nguyễn Thị Huyền Trang', 1, 1) ")
c.execute("select * from students ")
print(c.fetchall())


# # # ========== table teachers =======
c.execute('''create table teachers(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     teacherCode TEXT UNIQUE NOT NULL,
     teacherName TEXT NOT NULL,
     userId INT,
     classId INT,
     description TEXT,
     FOREIGN KEY(userId) REFERENCES users(id),
     FOREIGN KEY(classId) REFERENCES classes(id)
)''')
c.execute("insert into teachers(teacherCode, teacherName,userId,classId) values(?,?,?,?)",('230220','Nguyễn Vân Anh',2,1))
c.execute("select * from teachers")
print(c.fetchall())

# # # ========== table studentTest_relationship =======
c.execute(''' create table studentTest_rela(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     classTestRela_id INTEGER,
     studentId INTEGER, 
     mark REAL,
     description TEXT,
     FOREIGN KEY(classTestRela_id) REFERENCES classes(id),
     FOREIGN KEY(studentId) REFERENCES students(id)
)
''')

# # # ========== table questionLibrary =======
c.execute(''' create table quetionsLib(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     content NOT NULL,
     level INTEGER NOT NULL,
     teacherId INTEGER,
     description TEXT,
     FOREIGN KEY(teacherId) REFERENCES teachers(id)
)''')
questions =[('Học viện Kỹ thuật Quân sự', 3,1), ('236 Hoàng Quốc Việt, Bắc Từ Liêm, Hà Nội',5,1)]
for item in questions:
    c.execute("insert into quetionsLib(content, level, teacherId) values(?,?,?)",item)
c.execute("select * from quetionsLib")
print(c.fetchall())

# # ========== table testType =======
c.execute(''' create table testType(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     typeName TEXT NOT NULL,
     description TEXT
)''')

# # ========== table examination =======
c.execute('''create table examination(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     testName TEXT NOT NULL,
     testType_id INTEGER,
     teacherId INTEGER,
     description TEXT,
     FOREIGN KEY(testType_id) REFERENCES testType(id),
     FOREIGN KEY(teacherId) REFERENCES teachers(id)
)''')

# # ========== table questionsExamRelationship =======
c.execute('''create table questionsExam_Rela(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quesId INTEGER,
    examId INTEGER,
    description TEXT,
    FOREIGN KEY(quesId) REFERENCES questionsLib(id),
    FOREIGN KEY(examId) REFERENCES examinations(id)
)''')

# c.execute("select * from questionsExam_Rela")
# print(c.fetchall())

# # ========== table category =======
c.execute('''create table category(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     categoryName TEXT NOT NULL,
     description TEXT
)''')

# ========== table questions =======
c.execute(''' create table quetions(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     content TEXT NOT NULL,
     categoryId INTEGER,
     level INTEGER NOT NULL,
     description TEXT,
     FOREIGN KEY(categoryId) REFERENCES category(id)
)''')
 
conn.commit()
conn.close()