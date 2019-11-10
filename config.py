import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_APP='run.py'
    FLASK_DEBUG=1
    FLASK_ENV='development'
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'H\x98\x08\xf3I5\x07\x0f\xc4\xf0\x92\xde.>\x93b\x96\xfaE_\xc3j2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATION = False