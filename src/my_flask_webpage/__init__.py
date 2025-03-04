from my_flask_webpage.app import app, db
from my_flask_webpage.app.models import User

# when using flask shell, this decorator will add the db and User to the shell context
# so it can be used without exporting it extra
# (dont forget to export the FLASK_APP variable to the app.py file as environment variable)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}