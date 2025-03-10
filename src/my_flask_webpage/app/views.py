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
    return render_template('index.html', title='Jan Fenker', user=user)


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
        # ToDo: use flask login module
        session['user'] = {'username': username, 'email': user.email}
        return redirect(url_for('index'))
    return render_template('login.html', title="Internal Login", form=form)


@app.route('/projects')
def projects():
    return render_template('projects.html', title='Projects')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html', title='Impressum')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy')

@app.route('/internal')
def internal():
    return render_template('internal.html', title='Internal')


@app.route('/logout')
def logout():
    # logout user

    return redirect(url_for('index'))
