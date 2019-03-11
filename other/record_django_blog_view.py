#encoding=utf-8
import pymysql
import time

conn = pymysql.connect(host="127.0.0.1",user="blogeditor",password="20170218",database="dj-bobjiang-v2",charset="utf8")
cursor = conn.cursor()

sql = "select id,title,views from blog_post where visiable_id=1 order by id desc;"
cursor.execute(sql)
result = cursor.fetchall()
id_list = []
title_list = []
view_list = []
for r in result:
    id_list.append(r[0])
    title_list.append(r[1])
    view_list.append(r[2])
cursor.close()
conn.close()


ISOTIMEFORMAT="%Y-%m-%d-%X"
current_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
with open("/home/test/record_view/count_record_views.csv","a") as f:
    f.write(current_time+"\n")
    f.write(str(id_list).replace(" ","")[1:-1]+"\n")
    f.write(str(title_list).replace(" ","")[1:-1]+"\n")
    f.write(str(view_list).replace(" ","")[1:-1]+"\n")
    f.write("\n\n")
