import pymysql
db=pymysql.connect(host='192.168.0.163',
                   user='root',
                   password='430142',
                   port=3306
                   )
cursor = db.cursor()
sql = '''show databases;'''
sql1 = '''select * from dos where name = 1'''
cursor.execute(sql)
result=cursor.fetchall
print(result)


    
