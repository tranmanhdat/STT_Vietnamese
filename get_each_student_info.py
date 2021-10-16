import sqlite3

def get_each_student_info(studentId):
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select * from students where id ={0}".format(studentId))
        student= c.fetchone()
        fullname = student[2]
        code = student[1]
        classId = student[4]
        c.execute("select className from classes where id = {0}".format(classId))
        className = c.fetchone()[0]
        c.execute("select testId from studentTest_Rela where studentId ={0}".format(studentId))
        testIds= c.fetchall()
        c.execute("select mark from studentTest_Rela where studentId ={0}".format(studentId))
        marks= c.fetchall()
        testNames =[]
        for testId in testIds:
            c.execute("select type from Tests where id ={0}".format(testId))
            type_ = c.fetchone()[0]
            if type_ == 1:
                testNames.append("Kiểm tra giữa kỳ")
            else:
                testNames.append("Kiểm tra cuối kỳ")
    return fullname, code, className,marks, testNames    


if __name__ == "__main__":
    get_each_student_info(studentId)