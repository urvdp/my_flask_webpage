import os
from dotenv import load_dotenv

# Load .env variables into system environment
load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__)) # get the current directory of this file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-so-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False