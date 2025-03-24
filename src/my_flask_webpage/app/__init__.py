from flask import Flask
from flask_login import LoginManager
from src.my_flask_webpage.config import Config
from flask_sqlalchemy import SQLAlchemy

# __name__ variable passed to the Flask class is a Python predefined variable,
# which is set to the name of the module in which it is used
app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login' # handle dynamic login before accessing a protected page

app.config.from_object(Config)

db = SQLAlchemy(app)  # db object is the database instance of the Flask app

# The bottom import is a workaround to circular imports, a common problem with Flask applications.
from src.my_flask_webpage.app import views, models
