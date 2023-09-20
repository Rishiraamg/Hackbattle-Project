import MySQLdb
from flask import Flask, request, render_template, redirect, url_for

dcobj=MySQLdb.connect('localhost','root','admin')
cj=dcobj.cursor()

app = Flask(__name__)


user_credentials = {
    'user1': 'kirthick',
    'user2': '123',
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cj.execute("use VITRAVEL")
        cj.execute("select * from Login where Username=%s and Password=%s",(username,password))
        table=cj.fetchone()
        
       
        if table:
            return redirect(url_for('mainpage'))
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html', error=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cj.execute("use VITRAVEL")
        cj.execute("select * from Login where Username=%s",(username,))
        table=cj.fetchone()
        
        if table:
            error = "Username Already Exists"
            return render_template('signup.html', error=error)
        else:
            cj.execute(f"insert into Login (Username,Password) values (%s,%s)",(username,password))
            dcobj.commit()
            return redirect(url_for('login'))
            
    return render_template('signup.html', error=None)

@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    return render_template('mainpage.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    c=0
    if request.method == 'POST':
        
        name=request.form['nam']
        email=request.form['email']
        no=request.form['no']
        to=request.form['to']
        fro='VIT'
        date=str(request.form['date'])
        #vac=int(request.form['vac'])
        cj.execute("use VITRAVEL")
        cj.execute("insert into Travel (Name, Email, Mob, 'To', 'From', Date) values (%s,%s,%s,%s,%s,%s)",(name,email,no,to,fro,date))
        c=1
    if c==0:
        return render_template('apply.html',success=0)
    else:
        return render_template('apply.html',success=1)

def createdb():
    cj.execute('create database VITRAVEL')
    cj.execute('use VITRAVEL')
    cj.execute('create table Login (Username varchar(100), Password varchar(50))')
    cj.execute("create table Travel (Name varchar(100),'To' varchar(100), 'From' varchar(100), Date varchar(100), Mob varchar(100) , Email varchar(100), Vacancy int)")
    dcobj.commit()
    

def chkdat():
    cj.execute("show databases")
    chk=cj.fetchall()
    if chk:
        return 1
    else:
        return 0
    

if __name__ == '__main__':
    if chkdat()==0:
        createdb()
    app.run(debug=True)
    
