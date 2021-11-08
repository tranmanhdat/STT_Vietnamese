#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, time, datetime
from functools import partial
from os import curdir
from random import randint
from sqlite3.dbapi2 import connect
import sys
from flask import Flask, render_template, request, json, redirect, url_for, \
    session,send_file
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from flask.helpers import flash
# from flashlight_model import FlashlightModel
from audioUtils import standard_file
import sqlite3
# from flask_session import Session
from pydub import AudioSegment
from randomQuestions import randomQuestions
from randomStudents import randomStudents
from get_category import get_category
from students_get_Tests import students_get_Tests
from get_each_class_info import get_each_class_info
from get_each_student_info import get_each_student_info
import math
import os
import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567891011121'
app.config['UPLOAD_FOLDER'] = os.getcwd()+ '/static/audios'
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
fl_model = None


@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def index():
    if 'id' in session:
        id = session.get('id')
        username = session.get('username')
        des = session.get('des')
        fullname = session.get('fullname')
            # if an user
        if (des == '0'):
            return render_template("Profile_user.html", fullname = fullname)
            # if a teacher:
        if (des == '1'):
            return render_template("Profile_teacher.html",fullname = fullname)
            # if a student
        if (des == '2'):
            return render_template("Profile_student.html", fullname = fullname)
            # if an admin:
        if (des == '3'):
            return render_template("Profile_admin.html", fullname= fullname)
    return render_template("index.html")

@app.route("/login", methods=['POST', 'GET'])
def log_in():
    if 'id' in session:
        return redirect("/profile")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        is_exist = check_exist_in_db(username, password)
        if is_exist:
            # conn = sqlite3.connect("database.db")
            # conn.row_factory = sqlite3.Row
            # cur = conn.cursor()
            # cur.execute(
            #     "SELECT * FROM users where username='{0}' and password='{1}'".format(
            #         username, password))
            # rows = cur.fetchall()
            # for item in rows:
            #     id = item['id']
            #     username = item['username']
            #     # author = item['author']
            #     break

            #  get id and add to session
            with sqlite3.connect("database.db") as conn:
                c = conn.cursor()
                c.execute("select * from users where username = '{0}' and password = '{1}'".format(username, password))
                user = c.fetchone()
                des = user[3]
                fullname = user[4]
                print(fullname)
                id = user[0]
                print(id)
            session['id'] = id
            session['username'] = username
            session['des'] = des
            session['fullname'] = fullname
            # session["author"] = author
            return json.dumps({'status': True, 'profile': url_for('profile')})
        return json.dumps({'status': False})
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        fullname = json.loads(request.form['name'])
        print("fullname", fullname)
        username = json.loads(request.form['username'])
        print("username", username)
        password = json.loads( request.form['password'])
        print("password", password)
        # author = request.form['author']
        isExist = check_exist_in_db(username, password)
        if isExist == False:
            flag = True
            with sqlite3.connect("database.db") as conn:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO users(username,password,description,fullname)  values(?,?,?,?)",(username, password, '0',fullname))
                    conn.commit()
                except:
                    flag = False
                    conn.rollback()
            return json.dumps({'status': flag})
        return json.dumps({'status': False})
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('id')
    session.pop('username')
    session.pop('des')
    session.pop('fullname')
   
    return redirect("/")


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    id = session.get('id')
    if not id:
        return redirect("/login")
    else:
        # with sqlite3.connect('database.db') as conn:
        #     c = conn.cursor()
        #     c.execute("select * from users where id = {0}".format(id))
        #     user = c.fetchone()
        #     fullname = user[4]
        #     des = user[3]
        des = session.get('des')
        fullname = session.get('fullname')
        #  if this is an user
        # if an user
        if (des == '0'):
            return render_template("Profile_user.html", fullname = fullname)
        # if a teacher:
        if (des == '1'):
            return render_template("Profile_teacher.html",fullname = fullname)
        # if a student
        if (des == '2'):
            return render_template("Profile_student.html", fullname = fullname)
        # if an admin:
        if (des == '3'):
            return render_template("Profile_admin.html", fullname= fullname)
    # if session.get('username') and session.get('id'):
    #     with sqlite3.connect('database.db') as conn:
    #         c = conn.cursor()
    #         c.execute("select * from users where id = {0}".format(id))
    #         user  = c.fetchone()
    #         fullname = c.
    #     return render_template("Profile.html", fullname = fullname)
    # elif session.get('name') and session.get('author') == 1:
    #     return render_template("Profile_student.html", name=session['name'])
    # return render_template("index.html")


@app.route("/createLession", methods=['POST', 'GET'])
def createLession():
    if request.method == "POST":
        info = request.form['info']
        values = request.form['values']
        questionsLevels = request.form['questionsLevels']
        userId = session.get('id')
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId = {0}".format(userId))
            teacherId = c.fetchone()[0]
        content = ''
        inf = json.loads(info)
        vals = json.loads(values)
        questionsLevels = json.loads(questionsLevels)
        for i in range(len(vals)):
            content = content + vals[i] + '/*?space?*/'
        flag = True
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                c.execute(
                    "INSERT INTO lessions(teacherId,tittle,topic,content,level) values(?,?,?,?,?)",(teacherId, inf['tittle'], inf['topic'], content, inf['level_Test']))
                for i in range(0,len(vals)):
                    c.execute("insert into questionsLib(content, level, teacherId) values(?,?,?)",(vals[i],questionsLevels[i],teacherId))
                conn.commit()
            except:
                flag = False
                conn.rollback()
        
        if flag == True:
            return json.dumps({'status': True})
        else:
            print("False")
    else:  
        fullname = session.get('fullname')
        return render_template("createLession.html",fullname = fullname )


@app.route("/createTests", methods=['POST', 'GET'])
def createTests():
    id = session.get('id')
    fullname= session.get('fullname')
    with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId = {0}".format(id))
            teacherId = c.fetchone()[0]
            conn.commit()
    if request.method == "POST":
        info = request.form['info']
        info = json.loads(info)
        typeTest = int(info['typeTest'])
        codesNum = int(info['codesNum'])
        quesNum = int(info['quesNum'])
        levels = info['levels']
        classes = info['classes'] 
        classIds = ""
        classIds_int =[]
        for item in classes:
            classIds= classIds+item+" "
            classIds_int.append(int(item))

        time_todo = int(info['time_ToDo'])
        time_submit = info['time_Submit']
        tmp = time_submit.split('T')[0].split('-')
        time_submit = tmp[2] + '/' + tmp[1] + '/' + tmp[0]
        flag = True
        codes_arr = randomQuestions(codesNum, levels, quesNum, teacherId)
      
        codes_arr_str=[]
        for item in codes_arr:
            code_str=""
            for i in item:
                code_str = code_str+str(i)+" "
            code_str = code_str[:-1]
            codes_arr_str.append(code_str)
        flag= True
        with sqlite3.connect("database.db") as conn:
            try:
                c= conn.cursor()
                c.execute("insert into Tests(teacherId,type, codesNum, quesNum, classIds, time_todo, time_submit) values(?,?,?,?,?,?,?)",(teacherId, typeTest, codesNum, quesNum,classIds, time_todo, time_submit))
                #  tìm id của test => insert (classId, testId)
                c.execute("select id from Tests")
                arr = c.fetchall()
                testId = arr[len(arr)-1][0]
                for i in classIds_int:
                    c.execute("insert into classTest_Rela(classId, testId) values(?,?)",(i,testId))
                    c.execute("select id from students where classId = {0}".format(i))
                    students_id = c.fetchall()
                    for item in students_id:
                        c.execute("insert into studentTest_Rela( studentId, testId) values(?,?)",(int(item[0]),testId))
                
                students_each_code = randomStudents(codesNum, testId,  classIds_int)
                for i in range(0, codesNum):
                    c.execute("insert into testCodes(testId, code, quesIds, studentIds) values(?,?,?,?)",(testId, i, codes_arr_str[i], students_each_code[i]))
                conn.commit()
            except:
                flag= False
                conn.rollback()
        if flag == True:
            return json.dumps({'status': True})
    else:
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId = {0}".format(id))
            teacherId = c.fetchone()[0]
            c.execute("select id from classes where teacherId = {0}".format(teacherId))
            class_id = c.fetchall()
            for item in c.fetchall():
                class_id.append(item[0])

        classes = []
        for item in class_id:
            class_ =[]
            id = int(item[0])
            class_.append(id)
            with sqlite3.connect("database.db") as conn:
                c = conn.cursor()
                c.execute("select className from classes where id = {0}".format(id))
                className = c.fetchone()[0]
                class_.append(className)
                classes.append(class_)
    
        return render_template("createTests.html", fullname = fullname, classes = classes)

@app.route("/teacher_collection")
def teacher_collection():
        id = session.get('id')
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId ={0} ".format(id))
            teacher_id = c.fetchone()[0]
        fullname = session.get('fullname')
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select * from questionsLib where teacherId = {0}".format(teacher_id))
            temp_arr = c.fetchall()
        questions = []
        #  lưu content của các câu
        level1, level2, level3, level4, level5, level6, level7, level8, level9, level10 = [],[],[],[],[],[],[],[],[],[]
        num = 0
        for item in temp_arr:
            if (item[2]==1):
                level1.append(item[1])
            if (item[2]==2):
                level2.append(item[1])
            if (item[2]==3):
                level3.append(item[1])
            if (item[2]==4):
                level4.append(item[1])
            if (item[2]==5):
                level5.append(item[1])
            if (item[2]==6):
                level6.append(item[1])
            if (item[2]==7):
                level7.append(item[1])
            if (item[2]==8):
                level8.append(item[1])
            if (item[2]==9):
                level9.append(item[1])
            if (item[2]==10):
                level10.append(item[1])
        questions.append(len(level1))
        questions.append(len(level2))
        questions.append(len(level3))
        questions.append(len(level4))
        questions.append(len(level5))
        questions.append(len(level6))
        questions.append(len(level7))
        questions.append(len(level8))
        questions.append(len(level9))
        questions.append(len(level10))
        for i in questions:
            num = num+i

        # ===== tìm số bài thi đã tạo =====
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select * from Tests where teacherId = {0}".format(teacher_id))
            tests = c.fetchall()
        numTests = len(tests)
        for test in tests:
            print(test)
            day_prev = test[7]
            day_prev=day_prev.split("/")
            time1 = datetime.datetime(int(day_prev[2]),int(day_prev[1]
            ),int(day_prev[0]),23,59)   # hạn nộp bài
            time2 = datetime.datetime.now()  # thời gian hiện tại
            if time1>time2:
                flag = True  # cho phép làm

            else:
                flag=False  # không cho làm
                c.execute("select * from studentTest_Rela where testId={0}".format(int(test[0])))
                num_students=len(c.fetchall())
                c.execute("update Tests set description='{0}' where teacherId ={1} and id={2}".format(str(num_students),teacher_id,int(test[0]) ))
                conn.commit()
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select * from Tests where teacherId = {0}".format(teacher_id))
            tests = c.fetchall()
        return render_template("teacher_collection.html",fullname = fullname, questions=questions, num = num, numTests= numTests, tests = tests )

@app.route("/get_each_test_info/<int:testId>")
def get_each_test_info(testId):
    fullname = session.get('fullname')
    id = session.get('id')
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select id from teachers where userId ={0} ".format(id))
        teacher_id = c.fetchone()[0]
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select * from Tests where id={0}".format(testId))
        test=c.fetchone()
        if int(test[2])==1:
            testName = "giữa kỳ"
        if int(test[2])==2:
            testName = "cuối kỳ"
        if int(test[2])==3:
            testName = "tốt nghiệp"
        c.execute("select * from testCodes where testId ={0}".format(testId))
        all_codes=[]
        for item in c.fetchall():
            each_code=[]
            question_ids = []
            levels=[]
            contents=[]
            each_code.append("00"+str(item[2]))  # lấy mã đề  // 0
            temps = str(item[3]).split()  # mảng chứa id của các câu ở dạng string
            for id in temps:
                id = int(id)
                c.execute("select * from questionsLib where id ={0}".format(id))
                question = c.fetchone()
                if question:
                    contents.append(question[1])
                    levels.append(question[2])
            each_code.append(len(contents))   # 1
            each_code.append(contents)  # 2
            each_code.append(levels)  # 3
            all_codes.append(each_code)
        
        conn.commit()
    
    return render_template("get_each_test_info.html", fullname =fullname, test=test, testName=testName, all_codes=all_codes,testId=testId)

@app.route("/question_each_level/<int:level>", methods=['POST','GET'])
def question_each_level(level):
    if request.method == 'POST':
        newContent = json.loads(request.form["newContent"])
        quesId = int(json.loads(request.form["quesId"]))
        flag = True
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                if newContent:
                    c.execute("update questionsLib set content = '{0}' where id = {1}".format(newContent,quesId)) 
                conn.commit()

            except:
                flag = False
                conn.rollback()
        if flag:
            return json.dumps({"status": True})
    else:
        fullname = session.get('fullname')
        id = int(session.get('id'))
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId = {0}".format(id))
            teacherId = c.fetchone()[0]
        question_contents=[]
        question_ids =[]
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                c.execute("select * from questionsLib where teacherId = {0} and level = {1}".format(teacherId, level))
                for item in c.fetchall():
                    question_contents.append(str(item[1]))
                    question_ids.append(int(item[0]))
                conn.commit()
            except:
                conn.rollback()

        return render_template("question_each_level.html", fullname = fullname, question_contents= question_contents, level = level, num = len(question_contents), question_ids =question_ids)


@app.route("/classManagement")
def classManagement():
    fullname = session.get('fullname')
    id = session.get('id')
    all_classes=[]  # mảng chứa mỗi lớp mà giáo viên này quản lý
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select id from teachers where userId = {0}".format(id))
        teacherId = c.fetchone()[0]
        c.execute("select * from classes where teacherId = {0}".format(teacherId))
        classes_ = c.fetchall()
        for item in classes_:
            class_=[]
            class_.append(item[0])  # classId
            class_.append(item[1])  # lấy tên của lớp
            c.execute("select id from students where classId ={0}".format(item[0]))
            class_.append(len(c.fetchall()))  # số học viên
            all_classes.append(class_)
        
    return render_template("classManagement.html",fullname = fullname, all_classes = all_classes )

@app.route("/classInfo/<int:classId>")
def classInfo(classId):
    fullname = session.get('fullname')
    className, studentCodes, studentNames, testNames, marks= get_each_class_info(classId)

    return render_template("classInfo.html", fullname=fullname, className= className,studentNum = len(studentNames), studentCodes = studentCodes, studentNames = studentNames, testNames= testNames, marks = marks,numTests = len(testNames))

# @app.route("/studentInfo/<int: studentId>")
# def studentInfo(studentId):
#     fullname, code, className,marks, testNames = get_each_student_info(studentId)
#     num = len(marks)  # số bài kiểm tra đã làm

#     return render_template("Student_marks.html", fullname, code, className,marks, testNames )



@app.route("/selectExams", methods=['POST', 'GET'])
def selectExams():
    fullname = session.get('fullname')
    category_info = get_category()
    print("category_info", category_info)
    return render_template("SelectExams.html", fullname=fullname, category_info= category_info)


@app.route("/selectTests")
def selectTests():
    id = int(session.get('id'))

    fullname = session.get('fullname')
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select id from students where userId = {0}".format(id))
        studentId = c.fetchone()[0]
    Tests = students_get_Tests(studentId)
    return render_template("SelectTests.html", Tests = Tests, fullname = fullname)

@app.route("/test_time/<int:testId>", methods=['POST'])
def test_time(testId):
    if request.method == 'POST':
        id=int(session.get('id'))
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from students where userId = {0}".format(id))
            studentId = c.fetchone()[0]
        time1 =datetime.datetime.now()
        time_start = str(time1.strftime('%X'))
        flag=True
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                print("time_start khi update",time_start)
                print(testId, studentId)
                c.execute("select time_start from studentTest_Rela where testId ={0} and studentId={1}".format(testId, studentId))
                print("chưa đến đây")
                temp = c.fetchone()[0]
                print("temp", temp)
                if not temp:
                    c.execute("update studentTest_Rela set time_start='{0}' where testId ={1} and studentId ={2} ".format(time_start,testId, studentId))
                conn.commit()
            except:
                print("false")
                flag = False
                conn.rollback()
        if flag==True:
            return json.dumps({'status':True})

@app.route("/gettransFile", methods=['POST', 'GET'])
def get_trans_file():
    fullname = session.get('fullname')
    return render_template("getFileTrans.html", fullname = fullname)


@app.route("/Exams/<int:id>")
def Exams(id):
    fullname = session.get('fullname')
    # contents=[]
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select * from category where id ={0}".format(id))
        examName = c.fetchone()[1]
   
    contents=""
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT content  FROM questions where categoryId = {0}".format(id))
    rows=cur.fetchall() 
    print("rows", rows)
    for item in rows:
        contents= contents+str(item[0]) + '/*?space?*/'    
    print("contents", contents)
    return render_template("Exams.html", fullname = fullname, examName = examName, contents=contents)


@app.route("/Tests/<int:testId>/<int:code>", methods=['GET', 'POST'])
def Tests(testId, code):
        id=session.get('id')
        print("id",id)
        fullname = session.get('fullname')    
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select studentCode from students where userId ={0}".format(int(id)))
            studentCode = c.fetchone()[0]
            c.execute("select id from students where userId ={0}".format(int(id)))
            studentId = c.fetchone()[0]
            c.execute("select quesIds from testCodes where testId={0} and code ={1}".format(testId, code))
            quesIds = c.fetchone()[0]
        quesIds = quesIds.split(" ")
        id_arr=[]
        content_arr=[]
        for item in quesIds:
            if item!=' ':
                item = int(item)
                c.execute("select * from questionsLib where id ={0}".format(item))
                if len(c.fetchall())!=0:
                    id_arr.append(item)
                    with sqlite3.connect("database.db") as conn:
                        c=conn.cursor()
                        c.execute("select content from questionsLib where id={0}".format(item))
                        content = c.fetchone()[0]
                        content_arr.append(content)
        quesNum = len(content_arr)
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select * from Tests where id = {0}".format(testId))
            test = c.fetchone()
            c.execute("select time_start from studentTest_Rela where studentId={0} and testId ={1}".format(studentId,testId))
            time_start = c.fetchone()[0]
            if not time_start:
                now = datetime.datetime.now()
                time_start = now.strftime("%H:%M:%S")
        if int(test[2])==1:
            name = "Bài kiểm tra giữa kỳ"
        if int(test[2])==2:
            name = "Bài thi cuối kỳ"
        if int(test[2])==3:
            name="Bài thi tốt nghiệp"
        time_todo=test[6]
        return render_template("Tests.html", fullname = fullname, quesNum = quesNum, content_arr = content_arr, id_arr = id_arr, name = name, time_todo= time_todo, id= id, studentCode=studentCode, testId=testId, time_start=time_start)


@app.route("/transFile", methods=['POST', 'GET'])
def transFile():
    fullname = session.get('fullname')
    return render_template("TranslateFile.html", fullname = fullname)


@app.route("/userTests/<int:categoryId>")
def userTests(categoryId):
    fullname = session.get('fullname')
    return render_template("userTests.html", fullname=fullname)


@app.route("/createQuestionsTeachers", methods=['POST', 'GET'])
def createQuestionsTeachers():
    if request.method == 'POST':
        id = session.get('id')
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId ={0} ".format(id))
            teacher_id = c.fetchone()[0]
        fullname = session.get('fullname')
        contents = request.form['contents']
        contents_arr = json.loads(contents)

        levels = request.form['levels']
        levels_arr = json.loads(levels)
        for i in range(0, len(contents_arr)):
            flag = True
            with sqlite3.connect("database.db") as conn:
                try:
                    c = conn.cursor()
                    c.execute("insert into questionsLib(content, level, teacherId) values(?,?,?)",(contents_arr[i],
                    levels_arr[i],teacher_id))
                    conn.commit()
                except:
                    flag = False
                    conn.rollback()
        if flag == True:
            return json.dumps({'status': True})
    else:
        id = session.get('id')
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId ={0} ".format(id))
            teacher_id = c.fetchone()[0]
        fullname = session.get('fullname')
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select * from questionsLib where teacherId = {0}".format(teacher_id))
            temp_arr = c.fetchall()
        questions = []
        for item in temp_arr:
            question=[]
            question.append(item[0])
            question.append(item[1])  # content
            question.append(item[2]) # level
            questions.append(question)
        return render_template("createQuestionsTeachers.html", fullname = fullname, questions=questions, num = len(questions))

@app.route("/eraseQuestions", methods=['POST'])
def eraseQuestion():
    if request.method == "POST":
        delete_arr = json.loads(request.form["delete_arr"])
        id = int(session.get('id'))
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("select id from teachers where userId = {0}".format(id))
            teacherId = c.fetchone()[0]

        flag = True
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                for id in delete_arr:
                    quesId = int(id)
                    c.execute("delete from questionsLib where id ={0}".format(quesId))
                conn.commit()
            except:
                flag = False
                conn.rollback()
        if flag == True:
            return json.dumps({'status': True})


# ======= Admin =======
@app.route("/createExamsAdmin", methods=['POST', 'GET'])
def createExamsAdmin():
    fullname = session.get('fullname')
    if request.method == 'POST':
        categoryName = json.loads(request.form['categoryName'])
        contents = json.loads(request.form['contents'])
        levels = json.loads(request.form['levels'])
        flag = True
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                c.execute("insert into category(categoryName) values(?)", (categoryName,))
                c.execute("select id from category where categoryName = '{0}'".format(categoryName))
                categoryId = int(c.fetchone()[0])
                for i in range(0, len(contents)):
                    c.execute("insert into questions(content, categoryId,level) values(?,?,?)", (contents[i],categoryId, int(levels[i])))
                conn.commit()
            except:
                flag = False
                conn.rollback()
        if flag == True:
            return json.dumps({'status': True})

    else:
        category_info = get_category()
        return render_template("createExamsAdmin.html", fullname = session.get('fullname'), category_info = category_info, num = len(category_info))

@app.route("/downloadTest/<int:testId>")
def downloadTest(testId):
    print("testId",testId)
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select * from Tests where id={0}".format(testId))
        test=c.fetchone()
        if int(test[2])==1:
            testName = "Đề thi giữa kỳ"
        if int(test[2])==2:
            testName = "Đề thi cuối kỳ"
        if int(test[2])==3:
            testName = "Đề thi tốt nghiệp"
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("select * from Tests where id={0}".format(testId))
        test=c.fetchone()
        numQues= test[4]
        time_todo=test[6]
        time_submit =test[7] 
        c.execute("select * from testCodes where testId ={0}".format(testId))
        all_codes=[]
        for item in c.fetchall():
            each_code=[]
            question_ids = []
            levels=[]
            contents=[]
            each_code.append("00"+str(item[2]))  # lấy mã đề  // 0
            temps = str(item[3]).split()  # mảng chứa id của các câu ở dạng string
            for id in temps:
                id = int(id)
                c.execute("select * from questionsLib where id ={0}".format(id))
                question = c.fetchone()
                if question:
                    contents.append(question[1])
                    levels.append(question[2])
            each_code.append(len(contents))   # 1
            each_code.append(contents)  # 2
            each_code.append(levels)  # 3
            all_codes.append(each_code)    
    file_download = "static/testId_"+str(testId)+".xls"
    with open(file_download,"w+",encoding="utf-8" ) as f_write:
        f_write.write(testName+"\nSố câu"+str(numQues)+"\nThời gian làm bài: "+str(time_todo)+"\n")
        for i in range(0,len(all_codes)):
            f_write.write("Mã đề: "+str(all_codes[i][0])+"\n")
            f_write.write("STT\tNội dung\tMức độ\n")
            for j in range(0, all_codes[i][1]):
                f_write.write(str(j+1)+"\t"+str(all_codes[i][2][j])+"\t"+str(all_codes[i][3][j])+"\n")
    return send_file(file_download, as_attachment=True)    

@app.route("/testModify", methods=['POST'])
def testModify():
    if request.method == 'POST':
        testId = int(json.loads(request.form['testId']))
        new_date=json.loads(request.form['new_date'])
        new_date = new_date.split("-")
        new_date=str(new_date[2])+"/"+str(new_date[1])+"/"+str(new_date[0])
        new_time_todo=json.loads(request.form['new_time_todo'])
        flag= True
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                c.execute("update Tests set time_todo='{0}' where id ={1}".format(new_time_todo,testId))
                c.execute("update Tests set time_submit='{0}' where id ={1}".format(new_date,testId))
                conn.commit()
            except:
                print("False")
                flag=False
                conn.cursor()
        return json.dumps({"status":True})

@app.route("/deleteTests",methods=['POST'])
def deleteTests():
    if request.method=='POST':
        testIds_delete= json.loads(request.form['testIds_delete'])
        print(testIds_delete)
        flag= True
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                for id in testIds_delete:
                    c.execute("delete from Tests where id={0}".format(int(id)))
                    c.execute("delete from classTest_Rela where testId={0}".format(int(id)))
                    c.execute("delete from studentTest_Rela where testId={0}".format(int(id)))
                    c.execute("delete from testCodes where testId={0}".format(int(id)))
                conn.commit()
            except:
                flag=False
                print("False")
                conn.rollback()
        if flag:   
            return json.dumps({"status":True})

@app.route("/test")
def test():
    return render_template("Tests.html")

# check login
def check_exist_in_db(username, password):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users where username='{0}' and password='{1}'".format(
            username, password))
    rows = cur.fetchall()
    if not rows:
        return False  # not in DB
    return True  # in DB


@app.route('/recog', methods=['GET', 'POST'])
def recog_file():
    if request.method == 'POST':
        static_file = request.files['the_file']
        # here you can send this static_file to a storage service
        # or save it permanently to the file system
        filename = '/tmp/' + static_file.filename
        static_file.save(filename)
        standard_file(filename)
        # pred = fl_model.process_file("/tmp/temp.wav")
        pred = "result from engines"
        return pred


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    # res = 0
    if request.method == 'POST':
        # text_random = request.form['text_random'].lower()
        # text_trans = request.form['text_record'].lower()
        # dp = []
        # for i in range(0, len(text_random), 1):
        #     a = []
        #     for j in range(0, len(text_trans), 1):
        #         a.append(1000000)
        #     dp.append(a)
        # dp[0][0] = 0
        # dp[0][1] = 1
        # dp[1][0] = 1
        # for i in range(1, len(text_random), 1):
        #     for j in range(1, len(text_trans), 1):
        #         if text_random[i - 1] == text_trans[j - 1]:
        #             dp[i][j] = dp[i - 1][j - 1]
        #         dp[i][j] = min(dp[i][j],
        #                        min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
        # ts = len(text_trans) - dp[len(text_random) - 1][len(text_trans) - 1]
        # result = (ts / len(text_trans)) * 100
        # res = result
        #  tính thời gian làm bài của 

        #  xử lý điểm
        mark = 0.0

        flag = True
        # note: tạo folder và lưu vào đây
        id = int(session.get('id'))
        with sqlite3.connect("database.db") as conn:
            c= conn.cursor()
            c.execute("select studentCode from students where userId ={0}".format(id))
            studentCode = c.fetchone()[0] 
            c.execute("select id from students where userId ={0}".format(id))
            studentId= c.fetchone()[0]
        files = request.files.getlist('audio_data')
        print(files)
        print( "testId",request.form["testId"])
        testId=int(request.form["testId"])
        # nếu không có file nào => lưu điểm 0 vào database
        if len(files)==0:
            with sqlite3.connect("database.db") as conn:
                try:
                    c = conn.cursor()
                    c.execute("update studentTest_Rela set mark={0} where studentId = {1} and testId={2}".format(mark,studentId,testId))
                    conn.commit()
                except:
                    conn.rollback()
                    flag=False
        else:
            for file in files:
                if file:
                    # lấy testId từ filename
                    filename= secure_filename(file.filename)
                    print("filename",filename)
                    # testId = int(filename.split('_')[1])
                    folder_name = studentCode+"_"+str(testId)
                    folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']),folder_name)
                    if not os.path.exists(folder_upload):
                        os.mkdir(folder_upload)
                    folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']), folder_name)
                    # lưu file vào folder_upload
                    file.save(os.path.join(folder_upload,filename))

                    
            path_to_folder = os.path.join("static/audios",folder_name)
            with sqlite3.connect("database.db") as conn:
                    try:
                        c = conn.cursor()
                        #  lưu đường dẫn của folder vào db
                        c.execute("update studentTest_Rela set save_url='{0}' where studentId = {1} and testId={2}".format(path_to_folder,studentId,testId))

                        # lưu điểm vào db

                        c.execute("update studentTest_Rela set mark={0} where studentId = {1} and testId={2}".format(mark,studentId,testId))

                        c.execute("select * from testCodes where testId={0} ".format(testId))
                        for item in c.fetchall():
                            studentIds=item[4]
                            if str(studentId) in studentIds:
                                code = int(item[2])
                        print("test")
                        conn.commit()
                    except:
                        flag = False                          
                        conn.rollback()
        if flag==True:  
            data={
                'mark':mark
            }
            print("đã trả về mark")
            return json.dumps(data)
        else:
            print("false")
    # res = abs(res)
    # if res != 100:
    #     if res > 100:
    #         res = res % 100
    #     res = round(res, 2)

    # return json.dumps({'res1': res})
@app.route("/Test_Result/<int:testId>/<int:code>")
def show_result(testId,code):

    return render_template("Test_Result")

def splitAudio(filename, sec_per_split):
    filepath = '/tmp/' + filename
    audio = AudioSegment.from_file(filepath)
    total_secs = math.ceil(audio.duration_seconds)
    lst_file = []
    for i in range(0, total_secs, sec_per_split):
        split_filename = str(i) + '_' + filename
        t1 = i * 1000
        t2 = (i + sec_per_split) * 1000
        split_audio = audio[t1:t2]
        split_audio.export('/tmp/' + split_filename, format="wav")
        print(str(i) + ' Done')
        lst_file.append(split_filename)
        if i == total_secs - sec_per_split:
            print('All splited successfully')
    return lst_file


if __name__ == "__main__":
    # app.debug = True   # note
    # model_path = sys.argv[1]
    # fl_model = FlashlightModel(model_path)
    # app.run(host="0.0.0.0", port=5000, use_reloader=False)   #// note
    # app.run(host='0.0.0.0', port=5555)
    # app.run(host='0.0.0.0', port=5000, ssl_context=('/home/tmd/project/asr/172.17.0.1:5555.crt', '/home/tmd/project/asr/172.17.0.1:5555.key'))
    # app.run(host='0.0.0.0', port=5555, ssl_context=('/tmp/192.168.0.104:5555.crt','/tmp/192.168.0.104:5555.key'))
    app.run(debug=True)