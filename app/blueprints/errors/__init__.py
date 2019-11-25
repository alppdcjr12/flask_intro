from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import render_template, url_for
from app.forms import ContactForm
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from flask import render_template
from app import app, db, login
import os

bp = Blueprint('errors', __name__, template_folder='templates')

@bp.errorhandler(404)
def not_found_error(error):
    send_email(error)
    return render_template('/errors/error.html', error=error), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    send_email(error)
    return render_template('/errors/error.html', error=error), 500

def send_email(error):
    message = Mail(
        from_email='error@campaignforthequest.com',
        to_emails='petercharlandsilence@gmail.com',
        subject='Error: {}'.format(error),
        html_content=render_template('errors/error.html', error=error))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e.message)