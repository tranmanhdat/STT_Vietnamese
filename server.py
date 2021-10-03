#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import Flask, render_template, request, json, redirect, url_for, \
    session
# from flashlight_model import FlashlightModel
from audioUtils import standard_file
import sqlite3
from flask_session import Session
from pydub import AudioSegment
import math

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
fl_model = None


@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route("/home", methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def log_in():
    if session.get('name'):
        return redirect("/profile")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        is_exist = check_exist_in_db(username, password)
        if is_exist:
            conn = sqlite3.connect("database.db")
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM user where username='{0}' and password='{1}'".format(
                    username, password))
            rows = cur.fetchall()
            for item in rows:
                id = item['id']
                name = item['name']
                author = item['author']
                break
            session["id"] = id
            session["name"] = name
            session["author"] = author
            return json.dumps({'status': True, 'profile': url_for('profile')})
        return json.dumps({'status': False})
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        author = request.form['author']
        isExist = check_exist_in_db(email, password)
        if isExist == False:
            flag = True
            with sqlite3.connect("database.db") as conn:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO user (name,username,password,author)  values ('{0}','{1}','{2}',{3})".format(
                            name, email, password, author))
                    conn.commit()
                except:
                    flag = False
                    conn.rollback()
            return json.dumps({'status': flag})
        return json.dumps({'status': False})
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    if session.get('name') and session.get('author') == 0:
        return render_template("Profile.html", name=session['name'])
    elif session.get('name') and session.get('author') == 1:
        return render_template("Profile_student.html", name=session['name'])
    return render_template("index.html")


@app.route("/createExams", methods=['POST', 'GET'])
def createExams():
    if request.method == "POST":
        info = request.form['info']
        values = request.form['values']
        id_user = session.get('id')
        content = ''
        inf = json.loads(info)
        vals = json.loads(values)
        for i in range(len(vals)):
            content = content + vals[i] + '/*?space?*/'
        flag = True
        with sqlite3.connect("database.db") as conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO collection (id_user,tittle,topic,content,type,level)  values ({0},'{1}','{2}','{3}',{4},'{5}')".format(
                        id_user, inf['tittle'], inf['topic'], content,
                        inf['typeTest'], inf['level_Test']))
                conn.commit()
            except:
                flag = False
                conn.rollback()
        if flag == True:
            return json.dumps({'status': True})
    return render_template("CreateExams.html", name=session['name'])


@app.route("/createTests", methods=['POST', 'GET'])
def createTests():
    if request.method == "POST":
        info = request.form['info']
        inf = json.loads(info)
        # convert time to save db
        time_submit = inf['time_Submit']
        tmp = time_submit.split('T')[0].split('-')
        time = tmp[2] + '/' + tmp[1] + '/' + tmp[0]
        flag = True
        with sqlite3.connect("database.db") as conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO test_collection (id_collect,time_Todo,time_submit)  values ({0},{1},'{2}')".format(
                            inf['id_collection'], inf['time_ToDo'], time))
                conn.commit()
            except:
                flag = False
                conn.rollback()
        if flag == True:
            return json.dumps({'status': True})
    else:
        id_user = session.get('id')
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT *  FROM collection where type=2 and id_user={0}".format(
                id_user))
        rows = cur.fetchall()
        return render_template("CreateTests.html", rows=rows,
                               name=session['name'])


@app.route("/selectExams", methods=['POST', 'GET'])
def selectExams():
    return render_template("SelectExams.html", name=session['name'])


@app.route("/selectTests", methods=['POST', 'GET'])
def selectTests():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT ts.*,col.*  FROM test_collection ts,collection col where ts.id_collect=col.id")
    rows = cur.fetchall()
    return render_template("SelectTests.html", rows=rows, name=session['name'])


@app.route("/gettransFile", methods=['POST', 'GET'])
def get_trans_file():
    return render_template("getFileTrans.html", name=session['name'])


@app.route("/Exams", methods=['POST', 'GET'])
def Exams():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT *  FROM collection order by id desc limit 1")
    rows = cur.fetchall()
    for item in rows:
        ques = item
    return render_template("Exams.html", ques=ques, name=session['name'])


@app.route("/Tests/<id>", methods=['POST', 'GET'])
def Tests(id):
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT *  FROM collection where id={0}".format(id))
        rows = cur.fetchall()
        for item in rows:
            ques = item
    return render_template("Tests.html", ques=ques, name=session['name'])


@app.route("/transFile", methods=['POST', 'GET'])
def transFile():
    return render_template("TranslateFile.html", name=session['name'])


@app.route("/category", methods=['POST', 'GET'])
def category():
    return render_template("category.html", name=session['name'])


# check login
def check_exist_in_db(username, password):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM user where username='{0}' and password='{1}'".format(
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
    res = 0
    if request.method == 'POST':
        text_random = request.form['text_random'].lower()
        text_trans = request.form['text_record'].lower()
        dp = []
        for i in range(0, len(text_random), 1):
            a = []
            for j in range(0, len(text_trans), 1):
                a.append(1000000)
            dp.append(a)
        dp[0][0] = 0
        dp[0][1] = 1
        dp[1][0] = 1
        for i in range(1, len(text_random), 1):
            for j in range(1, len(text_trans), 1):
                if text_random[i - 1] == text_trans[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                dp[i][j] = min(dp[i][j],
                               min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
        ts = len(text_trans) - dp[len(text_random) - 1][len(text_trans) - 1]
        result = (ts / len(text_trans)) * 100
        res = result
    res = abs(res)
    if res != 100:
        if res > 100:
            res = res % 100
        res = round(res, 2)
    return json.dumps({'res1': res})


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
    app.debug = True
    # model_path = sys.argv[1]
    # fl_model = FlashlightModel(model_path)
    app.run(host="0.0.0.0", port=5000, use_reloader=False)
    # app.run(host='0.0.0.0', port=5555)
    # app.run(host='0.0.0.0', port=5000, ssl_context=('/home/tmd/project/asr/172.17.0.1:5555.crt', '/home/tmd/project/asr/172.17.0.1:5555.key'))
    # app.run(host='0.0.0.0', port=5555, ssl_context=('/tmp/192.168.0.104:5555.crt','/tmp/192.168.0.104:5555.key'))
