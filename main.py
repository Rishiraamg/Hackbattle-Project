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

def createdb():
    cj.execute('create database VITRAVEL')
    cj.execute('use VITRAVEL')
    cj.execute('create table Login (Username varchar(100), Password varchar(50))')
    dcobj.commit()
    




if __name__ == '__main__':
    #createdb()
    app.run(debug=True)
    
