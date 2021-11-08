import random
import sqlite3

def randomStudents(codesNum, testId, classIds_int):
    students_arr=[] 
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        for id in classIds_int:
            c.execute("select id from students where classId = {0}".format(id))
            students= c.fetchall()
            for student in students:
                students_arr.append(student[0])
    students_each_code=[]
    i=0
    temp=[]
    while i< len(students_arr):
        for j in range(0,codesNum):
            temp.append(j)
            i = i+1
            if i>=len(students_arr):
                break
    for j in range(0,codesNum):
        str1=""
        k=0
        for item in temp:
            if (item==j):
                str1= str1+str(students_arr[k])+" "
            k=k+1  
        str1=str1[:-1] 
        students_each_code.append(str1)
    

    return students_each_code
        
if __name__=="__main__":
   randomStudents(codesNum, testId,  classIds_int) 