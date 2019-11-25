import os
basedir = os.path.abspath(os.path.dirname(__file__))

#H\x98\x08\xf3I5\x07\x0f\xc4\xf0\x92\xde.>\x93b\x96\xfaE_\xc3j2

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATION = False

class DevelopmentConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATION = False

