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
    Each project has a:
    - title
    - a principal linked image: main_image
    - an alternative text for the image: alt
    - a description
    - a link to a project page: link (if the link is empty, then it is a generic project page and the project id is used
    to generate the link)
    - a link to an external page (if wished): link_ext
    - a list of images: gallery

    """
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    period = db.Column(db.String(64), nullable=True)
    main_image_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    description = db.Column(db.String(256))
    link = db.Column(db.String(64), nullable=True)
    link_ext = db.Column(db.String(128), nullable=True)

    gallery = db.relationship('Gallery', backref='project', lazy='joined', foreign_keys='Gallery.project_id')

    def __repr__(self):
        return '<Project {}>'.format(self.title)

    def __init__(self, title, period, image_id, description, link=None, link_ext=None):
        self.title = title
        self.period = period
        self.main_image_id = image_id
        self.description = description
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
