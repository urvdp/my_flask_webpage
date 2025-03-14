"""
This module contains the database models for the application.
So far:
- User: defines the user model
"""

from src.my_flask_webpage.app import db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    hex_code = db.Column(db.String(16), unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.hex_code = secrets.token_hex(8)  # generates a random 8 byte hex code

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    """
    This class is the basis for the project entries on the webpage.
    Each project consists of:

    - title: the title of the project
    - title_brief: a short title for the project
    - period: the time the project was active
    - main_image: a principal linked image
    - bg_image: a bannered background image for the project page or the main page (bg_images are not stored in gallery)
    - description: a short description of the project
    - link: a link to a project page (if the link is empty, then it is a generic project page and the project id is used
    to generate the link)
    - link_ext: a link to an external page (if wished)
    - gallery: a list of images associated with the project

    """
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    title_brief = db.Column(db.String(64))
    period = db.Column(db.String(64), nullable=True)
    main_image_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    bg_image = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(256))
    link = db.Column(db.String(64), nullable=True)
    link_ext = db.Column(db.String(128), nullable=True)

    gallery = db.relationship('Gallery', backref='project', lazy='joined', foreign_keys='Gallery.project_id')

    def __repr__(self):
        return '<Project {}>'.format(self.title)

    def __init__(self, title, title_brief, period, image_id, description, bg_image=None, link=None, link_ext=None):
        self.title = title
        self.title_brief = title
        self.period = period
        self.main_image_id = image_id
        self.description = description
        if bg_image and len(bg_image) < 1:
            self.bg_image = None
        else:
            self.bg_image = bg_image
        self.link = link
        self.link_ext = link_ext

    @property
    def image(self):
        return Gallery.query.get(self.main_image_id)


class Gallery(db.Model):
    __tablename__ = 'gallery'

    # this is a table that links one project to multiple images
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    src = db.Column(db.String(64), index=True, unique=True)
    alt = db.Column(db.String(64))
    cc = db.Column(db.String(128), nullable=True)
    cc_author = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<Gallery {}>'.format(self.alt)

    def __init__(self, src, alt, cc=None, cc_author=None, project_id=None):
        self.src = src
        self.alt = alt
        self.cc = cc
        self.cc_author = cc_author
        self.project_id = project_id  # links to the respective project the image belongs to
