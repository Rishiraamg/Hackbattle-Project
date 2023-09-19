from flask import Flask, request, render_template, redirect, url_for

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

        # Check if the entered credentials match the stored credentials
        if username in user_credentials and user_credentials[username] == password:
            return "Login Successful!"
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
