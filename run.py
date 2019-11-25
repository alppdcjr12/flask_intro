from app import app, db, login
from app.models import User, Post
from app import routes, models

@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Post=Post
    )