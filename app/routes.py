from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user

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


@app.context_processor
def global_variables():
    return dict(username=''
                )


@app.shell_context_processor
def make_shell_context():
    return_dict(
        app=app,
        db=db,
        User=User
    )


@app.route('/')
def index():
    context = {
        'names': ['Nicholas', 'Peter', 'Derek']
    }
    return render_template('index.html', **context)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    context = {
    }
    return render_template('about.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    context = {
        'form': form
    }
    return render_template('register.html', **context)
    if form.validate_on_submit():
        u = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        u.generate_password(u.password)
        db.session.add(u)
        db.session.commit()
        flash("You have registered successfully.", "info")
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
            flash("Incorrect email or password. Try again.", "danger")
        login_user(user, remember=form.remember_me.data)
        flash("You have logged in successfully.", "success")
        redirect(url_for('index'))

    context = {
        'form': form
    }
    return render_template('login.html', **context)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
    flash("Logout successful", "success")