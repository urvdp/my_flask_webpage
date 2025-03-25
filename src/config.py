import os
from dotenv import load_dotenv

# Load .env variables into system environment
load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))  # get the current directory of this file


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-so-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    ENV = 'development'
    try:
        DB_NAME = os.environ['POSTGRES_DB']  # db name
        DB_USER = os.environ['POSTGRES_USER']  # db user, default: postgres
        DB_PASSWORD = os.environ['POSTGRES_PASSWORD']  # db password
        DB_HOST = os.environ['DB_HOST']  # db host, in docker it is the service name of the db container (here postgres)
        DB_PORT = os.environ['DB_PORT']  # db port, default: 5432
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    except Exception as e:
        # in case an env variable is not set, the default SQLALCHEMY_DATABASE_URI will be used from the parent class
        print("Load config error: ", e)
        pass


class ProdConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config_map = {
    'development': DevConfig,
    'production': ProdConfig
}
