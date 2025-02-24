from src.my_flask_webpage import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = "Janniboy"
    return render_template('index.html', title='Home', user=user)

@app.route('/login')
def login():
    return render_template('login.html', title='Login')