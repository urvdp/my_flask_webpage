from src.my_flask_webpage.app import app
from flask import render_template, session, flash, url_for, redirect

from src.my_flask_webpage.app.forms import LoginForm
from src.my_flask_webpage.app import db
from src.my_flask_webpage.app import models


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
    # ToDo: read in projects from database
    #projects = models.Project.query.all()
    projects = [
        {
            'title': 'Web-Hosting on Raspberry Pi',
            'image': 'img/raspbi.jpg',
            'alt': 'Raspberry Pi',
            'description': 'I set up a web server on a Raspberry Pi 4 and hosted my own website on it.',
            'link': 'raspbi_webhost',
            'link_ext': None,
            'cc': None,
            'cc_author': None
        },
        {
            'title': 'Self-Collision Avoidance and Joint Limit Avoidance on ARMAR-6 humanoid',
            'image': 'img/ba/env_collisions.png',
            'alt': 'Bachelor\'s Thesis',
            'description': 'As part of my bachelor\'s thesis, I integrated safety constraints into a hierarchical '
                           'real-time controller.',
            'link': None,
            'cc': 'https://mujoco.org/',
            'cc_author': 'MuJoCo Simulation'
        },
        {
            'title': 'MSUP Workshop',
            'image': 'img/msup_system.jpg',
            'alt': 'MSUP Workshop',
            'description': 'Design of a cooperative mechatronic system in interdisciplinary teams',
            'link': 'msup',
            'link_ext': None,
            'cc': None,
            'cc_author': None
        },
        {
            'title': 'Development and Maintenance of Student Registration Platform',
            'image': 'img/spz_page.png',
            'alt': 'SPZ',
            'description': 'Added new features to the student registration platform for '
                           'the Sprachenzentrum at KIT.',
            'link': None,
            'link_ext': 'https://github.com/spz-signup',
            'cc': None,
            'cc_author': None
        }
    ]
    return render_template('projects.html', title='Projects', projects=projects)


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

# project views go here

@app.route('/projects/msup')
def msup():
    project_title = 'MSUP Workshop'
    return render_template('projects/msup.html', title='MSUP', project_title=project_title)

@app.route('/projects/raspbi_webhosting')
def raspbi_webhost():
    project_title = 'Web-Hosting on Raspberry Pi'
    bg_image = 'img/raspbi_banner.jpg'
    return render_template('projects/raspbi_webhost.html',
                           title='Raspberry Pi Web-Hosting',
                           project_title=project_title,
                           bg_image=bg_image)

