from app import app, db
from app.models import User, Project, Gallery

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project, 'Gallery': Gallery}