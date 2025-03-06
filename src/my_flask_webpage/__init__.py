from my_flask_webpage.app import app, db
from my_flask_webpage.app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}