import sqlite3


def get_each_class_info(classId):
    class_info =[]
    class_info.append(classId)  # lấy classId - 0
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select className from classes where id = {0}".format(classId))
        className = c.fetchone()[0]
        class_info.append(className)  # lấy className - 1
        c.execute("select * from students where classId ={0}".format(classId))
        temp_arr= c.fetchall()  # các học sinh thuộc lớp này
        studentCodes = []
        studentNames = []
        studentIds = []
        for item in temp_arr:
            studentIds.append(item[0])  # lấy id của học viên của lớp này
            studentCodes.append(item[1])  # lấy mã học viên
            studentNames.append(item[2])  # lấy tên học viên
        class_info.append(studentCodes)  # 2 mảng mã học viên
        class_info.append(studentNames)  # 3 mảng tên học viên
        c.execute("select testId from classTest_Rela where classId = {0}".format(classId))
        testId_arr = c.fetchall()
        testNames =[]
        marks=[]
        for item in testId_arr:
            c.execute("select type from Tests where id ={0}".format(item[0]))
            type_ = c.fetchone()[0]
            if type_ == 1:
                testNames.append("Kiểm tra giữa kỳ")
            if type_==2:
                testNames.append("Kiểm tra cuối kỳ")
            if type_==3:
                testNames.append("Bài thi tốt nghiệp")
        for studentId in studentIds:
            mark=[]
            print("studentId", studentId)
            for i in range(0, len(testId_arr)):   
                c.execute("select mark from studentTest_Rela where testId = {0} and studentId = {1} ".format(testId_arr[i][0], studentId))
                temp = c.fetchone()
                if not temp:
                    mark.append(None)
                else:
                    mark.append(temp[0])
            marks.append(mark)
        print("marks", marks)
    return className, studentCodes, studentNames, testNames, marks


if __name__ == "__main__":
   get_each_class_info(classId)