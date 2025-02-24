import os

from flask import Flask

STATIC_DIR = os.path.abspath('/src/static')

print(STATIC_DIR)

app = Flask(__name__, static_folder=STATIC_DIR)

from src import views

if __name__ == "__init__":
    app.run()

