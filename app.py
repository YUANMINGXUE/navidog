import requests
from flask import *
import pymysql
app=Flask(__name__)
app.config.from_pyfile('config.py')
def connector(host,user,port, passwd):
    db=pymysql.connect(host=host,
                    user=user,
                    port=port,
                    password=passwd)
    cursor =db.cursor()
    return cursor
@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('newlogin.html')
    host=request.form.get('host')
    user=request.form.get('user')
    pwd=request.form.get('pwd')
    port=int(request.form.get('port'))
    session['host']=host
    session['user'] = user
    session['pwd'] = pwd
    session['port'] = port
    cursor= connector(host=host,user=user,passwd=pwd,port=port)
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
        tables2=[]
        for i in tables:
            tables2.append(str(i)[2:-3])
        dicts[database] = tables2


    return render_template('newdatabase.html',list=list,dicts=dicts)
@app.route('/show', methods=['GET','POST'])
def show():
    cursor=connector(session.get('host'),session.get('user'),session.get('port'),session.get('pwd'))
    database= request.args.get('database')
    table = request.args.get('table')
    cursor.execute('use '+database)
    sql = "SELECT * FROM %s" % (table)
    cursor.execute(sql)
    des= cursor.description
    HEADER =[]
    for head in des:

        HEADER.append(head[0])
    print(des)
    result=cursor.fetchall()
    newres = []
    for i in result:
        newres.append(list(i))
    return jsonify({'result': newres ,'heads' : HEADER})
@app.route("/iframe/<database>/<table>", methods=['GET','POST'])
def iframe(database, table):
    cursor = connector(session.get('host'), session.get('user'), session.get('port'), session.get('pwd'))
    # database = request.args.get('database')
    # table = request.args.get('table')
    cursor.execute('use ' + database)
    sql = "SELECT * FROM %s" % (table)
    cursor.execute(sql)
    des = cursor.description
    HEADER = []
    for head in des:
        HEADER.append(head[0])
    print(des)
    result = cursor.fetchall()
    newres = []
    for i in result:
        newres.append(list(i))
    return render_template('iframe.html', header=HEADER, result=newres)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
