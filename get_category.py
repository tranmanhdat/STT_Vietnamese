import sqlite3

def get_category():
    category_info = []
    conn = sqlite3.connect("database.db")
    c= conn.cursor()
    c.execute("select * from category")
    category_arr = c.fetchall()
    category_id =[]
    for item in category_arr:
        category_each = []
        category_id.append(item[0])
        category_each.append(item[0])   ### 0: id
        category_each.append(item[1])   ###  1: categoryName
        category_info.append(category_each)
    for i in range(0,len(category_id)):
        print("category_info[id]",category_info[i] )
        content_each=[]
        c.execute("select content from questions where categoryId = {0}".format(category_id[i]))
        temp = c.fetchall()
        print("temp",temp)
        category_info[i].append(len(temp))  ### 2: số câu hỏi
        for j in temp:
            content_each.append(j[0])
        category_info[i].append(content_each)   # 3: nội dung của các câu
    print(category_info)
    return category_info

if __name__ == "__main__":
    get_category()