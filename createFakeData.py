import sqlite3
from flask import current_app,g
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

# users=[
#     ('quoctrung','quoctrung','người dùng'),
#     ('phuongthao','phuongthao','người dùng'),
#     ('ngochanh','ngochanh','người dùng'),
# ]

# teachers = [
#     ('011101','Võ Diệu Quỳnh',6,2),
#     ('050201','Lê Thị Trà My', 7,3),
#     ('200201','Lê Văn Hoàng',8,5)
# ]

# students = [
#     ('281001','Nguyễn Thị Nhật Lệ',9,2),
#     ('280401','Nguyễn Hoàng Thu Thảo',10,3),
#     ('251201','Nguyễn Bùi Thúy Hiền',11,4)
# ]
# for item in teachers:
#     c.execute("insert into teachers(teacherCode, teacherName,userId, classId) values(?,?,?,?)",item)

# className = [('CNTT'),('ANHTTT'),('BĐATTT'),('PTDL')]
# c.execute("insert into classes(className) values('PTDL')")

# questions=[
#     ('Nếu em đi trái tim này buồn biết mấy',3,2),
#     ('Dù biết trong lòng còn yêu còn thương lắm đấy',5,3),
#     ('Ngược dòng thời gian quay về quá khứ',7,4)
# ]
# for item in questions:
#     c.execute("insert into questionsLib(content, level, teacherId) values(?,?,?)",item)

# c.execute("insert into testType(typeName) values('003')")
# c.execute("insert into examination(testName, testType_id, teacherId) values('Kiểm tra giữa kỳ',2,4)")
# # c.execute("insert into examination(testName, testType_id, teacherId) values('Kiểm tra cuối kỳ',1,2)")
# c.execute("insert into classTest_Rela(classId, examId) values(2,1) ")
# c.execute("insert into classTest_Rela(classId, examId) values(3,2) ")
# c.execute("insert into classTest_Rela(classId, examId) values(4,1) ")

# c.execute("insert into studentTest_Rela(classTestRela_id,studentId) values(1,2)")
# c.execute("insert into studentTest_Rela(classTestRela_id,studentId) values(2,3)")
# c.execute("insert into studentTest_Rela(classTestRela_id,studentId) values(2,4)")

# c.execute("insert into category(categoryName) values('Âm nhạc')")
# c.execute("insert into category(categoryName) values('Văn học')")
# c.execute("insert into category(categoryName) values('Toán học')")
# items = [
#     ('Người lạ ơi xin cho tôi mượn bờ vai', 1,7),
#     ('Nghệ thuật là ánh trăng lừa dối', 2,6),
#     ('Tam giác là hình có ba cạnh',3,2)
# ]


# for item in items:
#     c.execute("insert into questions(content, categoryId, level) values(?,?,?)", item)
# c.execute("update users set username = ")
# c.execute("drop table users")
# items =[
#     ('huyentrang','huyentrang','người dùng'),
#     ('xuanlam','xuanlam','người dùng'),
#     ('quoctrung','quoctrung','người dùng'),
#     ('phuongthao','phuongthao','người dùng'),
#     ('ngochanh', 'ngochanh','người dùng'),
#     ('011101','dieuquynh','giảng viên'),
#     ('050202','tramy','giảng viên'),
#     ('200201','vanhoang','giảng viên'),
#     ('281001','nhatle','học viên'),
#     ('280401','thuthao','học viên'),
#     ('250201','thuyhien','học viên')
# ]

# for item in items:
#     c.execute("insert into users(username, password,description) values(?,?,?)",item)
# c.execute("update users set description = 2 where description ='học viên'")
# c.execute("insert into users(username, password, description, fullname) values(?,?,?,?)",('giabao','giabao','3','Nguyễn Văn Gia Bảo'))
c.execute("select * from questionsLib")
print(c.fetchall())
conn.commit()
conn.close()