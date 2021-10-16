import sqlite3
import random

#  codesNum: số mã đề
#  quesNum: 1 đề có bao nhiêu câu
#  levels: số câu mỗi mức độ
def randomQuestions(codesNum, levels, quesNum, teacherId):
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
            #  lọc ra từng loại 
        levels_arr=[]
        for i in range(0,10):
            temp=[]
            c.execute("select id from questionsLib where level = {0} and teacherId ={1}".format(i, teacherId))
            temp = c.fetchall()
            levels_arr.append(temp)

        # codes_arr mảng lưu id của các câu hỏi của từng mã đề
        codes_arr=[]
        for i in range(0,codesNum):
            code=[]
            for k in range(0,10):
                    level_num_ques = int(levels[k]) # số câu của 1 mức độ
                    if level_num_ques==0:
                        continue
                    if len(levels_arr[k])==0:
                        continue
                    count1 =0
                    while count1 < level_num_ques:
                        temp = random.randrange(0,len(levels_arr[k]),1)
                        temp1= levels_arr[k][temp]
                        questionId = temp1[0]
                        if questionId in code:
                            if level_num_ques > len(levels_arr[k]):
                                break  
                            continue
                        else:
                            code.append(questionId)
                            count1 = count1+1
                    if len(code) >quesNum:
                        break   

                        

            print("code ne: ")
            print(code)
            codes_arr.append(code)
    return codes_arr

if __name__== "__main__":
    randomQuestions(codesNum, levels,quesNum, teacherId)
    