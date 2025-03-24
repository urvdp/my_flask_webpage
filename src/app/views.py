from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from app import app
from app import models
from app.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    highlights = ['raspbi_webhost', 'msup']

    picked_projects = []
    for link in highlights:
        picked_projects.append(models.Project.query.filter_by(link=link).one())

    return render_template('index.html', title='Jan Fenker', projects=picked_projects)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('internal'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user.data
        pw = form.password.data
        user = models.User.query.filter(models.User.username == username).first()
        if user is None or not user.check_password(pw):
            flash('Invalid username or password :/')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('internal')
        return redirect(url_for(next_page.strip('/')))
    return render_template('login.html', title="Internal Login", form=form)


@app.route('/logout')
def logout():
    # logout user
    logout_user()
    return redirect(url_for('index'))


@app.route('/projects')
def projects():
    projects = models.Project.query.all()
    return render_template('projects.html', title='Projects', projects=projects)


@app.route('/projects/<link>')
def project(link):
    project_db = models.Project.query.filter_by(link=link).one()
    return render_template('projects/' + project_db.link + '.html', title=project_db.title_brief,
                           project=project_db)


@app.route('/impressum')
def impressum():
    return render_template('impressum.html', title='Impressum')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy')


@app.route('/internal')
@login_required
def internal():
    return render_template('internal.html', title='Internal')
