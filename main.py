import MySQLdb
from flask import Flask, request, render_template, redirect, url_for

dcobj=MySQLdb.connect('localhost','root','admin')
cj=dcobj.cursor()

app = Flask(__name__)

# A simple dictionary to store username-password pairs (replace with a database in a real application).
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
        
        # Check if the entered credentials match the stored credentials
        #if username in user_credentials and user_credentials[username] == password:
        if table:
            return "Login Successful!"
            #redirect here
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
        
        # Check if the entered credentials match the stored credentials
        #if username in user_credentials and user_credentials[username] == password:
        if table:
            error = "Username Already Exists"
            return render_template('signup.html', error=error)
        else:
            cj.execute(f"insert into Login (Username,Password) values (%s,%s)",(username,password))
            dcobj.commit()
            return redirect(url_for('login'))
            
    return render_template('signup.html', error=None)

def createdb():
    cj.execute('create database VITRAVEL')
    cj.execute('use VITRAVEL')
    cj.execute('create table Login (Username varchar(100), Password varchar(50))')
    cj.execute("create table Travel (Name varchar(100),To varchar(100), From varchar(100), Date date, Mob int, Vacancy int)")
    dcobj.commit()
    

if __name__ == '__main__':
    #createdb()
    app.run(debug=True)
    
