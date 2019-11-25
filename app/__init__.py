from logging.handlers import RotatingFileHandler
from flask_moment import Moment
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import ProductionConfig, DevelopmentConfig
from flask import Flask
import os
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'account.login'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.blueprints.account import bp as account_bp
app.register_blueprint(account_bp, url_prefix='/account')

from app.blueprints.users import bp as users_bp
app.register_blueprint(users_bp, url_prefix='/users')

from app.blueprints.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app.blueprints.errors import bp as errors_bp
app.register_blueprint(errors_bp, url_prefix='/errors')

if os.environ['FLASK_ENV'] == 'development':
    app.config.from_object(DevelopmentConfig)
elif os.environ['FLASK_ENV'] == 'production':
    app.config.from_object(ProductionConfig)

moment = Moment(app)

if not app.debug:
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/flask_intro_errors.log', maxBytes=10240,
    backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask Intro')


