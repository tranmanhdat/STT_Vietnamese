import sqlite3
import random

#  codesNum: số mã đề
#  quesNum: 1 đề có bao nhiêu câu
#  levels: số câu mỗi mức độ
def randomQuestions(codesNum, levels, quesNum, teacherId):
    levels_num_ques=[] # mảng lưu số câu mỗi mức độ
    for item in levels:
        if item!='':
            levels_num_ques.append(int(item))
        else:
            levels_num_ques.append(0)
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
            #  lọc ra từng loại 
        levels_arr=[]  # mảng id của từng mức độ từ 1-10
        for i in range(0,10):
            temp=[]
            c.execute("select id from questionsLib where level = {0} and teacherId ={1}".format(i+1, teacherId))
            temp = c.fetchall()
            levels_arr.append(temp)
        
        # codes_arr mảng lưu id của các câu hỏi của từng mã đề
        codes_arr=[]
        for i in range(0,codesNum):
            code=[]
            for k in range(0,10):
                    count1 =0
                    while count1 < levels_num_ques[k]:
                        temp = random.randrange(0,len(levels_arr[k]),1)
                        temp1= levels_arr[k][temp]
                        questionId = temp1[0]
                        if questionId in code:
                            if levels_num_ques[k] > len(levels_arr[k]):
                                break  
                            continue
                        else:
                            code.append(questionId)
                            count1 = count1+1
                    if len(code) >quesNum:
                        break   

                        

            codes_arr.append(code)
    return codes_arr

if __name__== "__main__":
    randomQuestions(codesNum, levels,quesNum, teacherId)
    