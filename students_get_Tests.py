import sqlite3
import datetime

from flask.helpers import flash


#  lấy thông tin tất cả những bài Test mà học viên này phải làm show lên bảng
def students_get_Tests(studentId):
    Tests=[]
    with sqlite3.connect("database.db") as conn:
        try:
            c= conn.cursor()
            c.execute("select * from testCodes")
            arr = c.fetchall()
            for item in arr:
                test=[]
                studentIds_each_code = item[4].split() 
                temp= str(studentId)
                #  nếu có id của học viên trong mã đề này
                if temp in studentIds_each_code:
                    testId = int(item[1])
                    test.append(testId)  # lấy id của test - 0
                    c.execute("select * from Tests where id = {0}".format(testId))
                    temp1= c.fetchone()
                    #  lấy loại bài - 1
                    if temp1[2]== 1:
                        test.append("Giữa kỳ")
                    if temp1[2]== 2:
                        test.append("Cuối kỳ")
                    if temp1[2]== 3:
                        test.append("Tốt nghiệp")
                    #  lấy mã đề - 2
                    test.append(item[2])

                    #  lấy số câu  - 3
                    test.append(int(temp1[4])) 

                    #  lấy thời gian làm bài - 4
                    test.append(int(temp1[6]))

                    #  lấy thời gian nộp - 5
                    test.append(temp1[7])
                    day_prev = temp1[7]
                    day_prev=day_prev.split("/")
                    time1 = datetime.datetime(int(day_prev[2]),int(day_prev[1]),int(day_prev[0]),23,59)   # hạn nộp bài
                    time2 = datetime.datetime.now()  # thời gian hiện tại
                    if time1>time2:
                        flag = True  # cho phép làm
                    else:
                        flag=False  # không cho làm

                    #  kiểm tra xem đã làm hay chưa - 6
                   
                    c.execute("select mark from studentTest_Rela where testId={0} and studentId={1}".format(testId,studentId))

                    mark = c.fetchone()[0]
                    if mark==None:
                        if flag ==True:
                            test.append("Làm bài")
                        if flag==False:
                            test.append("Quá hạn")
                    else:
                        test.append(mark)
                    Tests.append(test)
        except:
            print("False")
            conn.rollback()

    return Tests
if __name__== "__main__":
    students_get_Tests(studentId)