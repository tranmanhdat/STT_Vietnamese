import random
import sqlite3

def randomStudents(codesNum, testId, classIds_int):
    print("đã đến đây chưa?")  # rồi nha
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        print("classIds_int", classIds_int)
        for id in classIds_int:
            print("id", id)
            c.execute("select id from students where classId = {0}".format(id))
            students_arr = c.fetchall()
            print("students_arr", students_arr)  # đến đây rồi
    students_each_code=[]
    start =0
    for i in range(0, codesNum):
        temp = ""
        count=0
        for j in range(start, len(students_arr)):
            temp = temp + str(students_arr[j][0])+ " "
            count = count+1
        temp = temp[:-1]  # xóa ký tự trống ở cuối chuỗi
        students_each_code.append(temp)
        start = start+ count
    

    return students_each_code
        
if __name__=="__main__":
   randomStudents(codesNum, testId,  classIds_int) 