from my_flask_webpage.app import app
from flask import render_template, session, flash, url_for, redirect

from my_flask_webpage.app.forms import LoginForm
from my_flask_webpage.app import db
from my_flask_webpage.app import models


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = session.get('user')  # session object used to store user data
    if user:
        flash('You are logged in as {}'.format(user['username']))
    return render_template('index.html', title='Login Challenge', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user') is not None:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user.data
        pw = form.password.data
        user = models.User.query.filter_by(username=username).first()
        if user is None or not user.check_password(pw):
            flash('Invalid username or password :/')
            return redirect(url_for('login'))
        # ToDo: use the remember me data
        session['user'] = {'username': username, 'email': user.email}
        return redirect(url_for('index'))
    return render_template('login.html', title="Jan's Login Castle", form=form)


@app.route('/forgot_pw')
def forgot_password():
    return render_template('forgotPW.html', title='Pieceful Realm')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/crownhall')
def crownhall():
    user = session.get('user')
    user_db = models.User.query.filter_by(username=user["username"]).first()
    return render_template('crownhall.html', title='Crownhall', user=user_db)