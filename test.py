import pymysql
def connector(host,user,port, passwd):
    db=pymysql.connect(host=host,
                    user=user,
                    port=port,
                    password=passwd)
    cursor =db.cursor()
    return cursor
cursor=connector('192.168.0.163','root',3306,'430142')
list=[]
try:
    cursor.execute("show databases")
    databases = cursor.fetchall()
    print("数据库列表")
    print("??")
    for database in databases:
       list.append((database[0]))
    print("??")
except Exception as e:
    print(e)
dicts={}
for database in list:
    cursor.execute('use '+str(database))
    cursor.execute("show tables")
    tables=cursor.fetchall()
    dicts[database]=tables
print(dicts)


