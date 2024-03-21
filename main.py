import os.path
from flask import *
import  mysql.connector

app=Flask(__name__)

app.config['UPLOAD_FOLDER']="static/images/"
app.secret_key="MKMS@123"

def getConn():
    conn=mysql.connector.connect(host="localhost",username="root",password="",port="3306",database="email")
    return conn


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/newuser",methods=["POST","GET"])
def newuser():
    msg=''
    if request.method=="POST":
        name=request.form.get("name")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        email=request.form.get("email")
        image=request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],image.filename))

        sql="insert into det(name,username,password,email,image)values('%s','%s','%s','%s','%s')" %(name,uname,pwd,email,image.filename)
        print(sql)

        conn = getConn()
        cursor = conn.cursor()
        cursor.execute(sql)

        conn.commit()
        conn.close()
        msg="Data Inserted Success"

    return render_template("register.html",msg=msg)

@app.route("/login",methods=["POST","GET"])
def login():
    msg=''
    if request.method=="POST":
        uname=request.form['uname']
        pwd=request.form['pwd']
        sql="select * from det where username like '%s' and password like '%s'"%(uname,pwd)
        conn=getConn()
        cursor=conn.cursor()
        cursor.execute(sql)
        data=cursor.fetchone()
        if(data):
            session['id']=data[0]
            session['image']=data[5]
            return render_template("main.html")
        else:
            msg="Invalid username/password"
    return render_template("login.html",msg=msg)

@app.route("/viewuser")
def viewuser():
    id=session['id']
    sql="select * from det where id ="+str(id)
    conn=getConn()
    cursor=conn.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    return render_template("viewuser.html",data=data)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")



if __name__=="__main__":
    app.run(debug=True)
