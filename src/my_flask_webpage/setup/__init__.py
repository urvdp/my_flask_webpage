from src.my_flask_webpage.app import app, db
from src.my_flask_webpage.app.models import User, Project, Gallery

# set the application context
app.app_context().push()
