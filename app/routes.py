from flask import render_template, redirect, url_for, flash, request
from app import app, db, login
from app.forms import ContactForm
from app.models import User, Post, followers
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app.email import send_email
import requests, json
from app.blueprints.users.forms import BlogForm

# FLASK_LOGIN
# .is_authenticated
# .is_anonymous
# .is_anonymous
# .get_id()

# CRUD APPLICATION
# C - CREATE: POST
# R - READ: GET
# U - UPDATE: PUT
# D - DELETE: DELETE

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = BlogForm()
    context = {
        'form': form,
        'posts': current_user.followed_posts(),
    }
    if form.validate_on_submit():
        p = Post(body=form.body.data, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash("Posted successfully", "success")
        return redirect('/')
    return render_template('users/index.html', **context)

@app.route('/partials/navbar')
def nav():
    context = {

    }
    return render_template(url_for('navbar'), **context)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    context = {
        'recipient_name': 'Peter Charland',
        'sender_name': form.name.data,
        'message': form.message.data,
        'sender_email': form.email.data,
        'form': form
    }
    if form.validate_on_submit():
        send_email()
        flash("Your message has been sent.")
        return redirect(url_for('contact'))
    return render_template('contact.html', **context)

# @app.before_request()
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()

