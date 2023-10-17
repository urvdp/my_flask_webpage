from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello to Jan's world!"


if __name__ == "__init__":
    app.run()
