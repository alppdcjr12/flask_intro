from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.blueprints.users.forms import BlogForm, ProfileForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Post
from app import db, login

bp = Blueprint('users', __name__, template_folder='templates')

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    context = {
        'form': form,
    }
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.password = form.password.data
        current_user.generate_password(current_user.password)
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.merge(current_user)
        db.session.commit()
        return redirect(url_for('users.profile', id=current_user.id))

    return render_template('users/edit_profile.html', **context)

@bp.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    form = BlogForm()
    context = {
        'posts': Post.query.filter_by(user_id=id).order_by(Post.timestamp.desc()),
        'form': form
    }
    if request.method == 'POST':
        if form.validate_on_submit():
            p = Post(body=form.body.data, user_id=current_user.id)
            db.session.add(p)
            db.session.commit()
            flash("Posted successfully", "success")
            return redirect(url_for('profile', id=current_user.id))
    return render_template('users/profile.html', id=id, **context)

@bp.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    p = Post.query.get(id)
    db.session.delete(p)
    db.session.commit()
    flash("Post deleted successfully", "info")
    return redirect(url_for('user.profile', id=current_user.id))

@bp.route('/users')
@login_required
def users():
    context = {
        'users': [i for i in User.query.all() if (i.id != current_user.id)],
    }
    return render_template('users/users.html', **context)

@bp.route('/users/add/<user>')
@login_required
def users_add(user):
    user = User.query.filter_by(name=user).first()
    if user not in current_user.user_following:
        flash("User added successfully", "success")
        current_user.follow(user)
        return redirect(url_for('users.users'))
    else:
        flash(f"You are already following {user.name}", "warning")
        return redirect(url_for('users.users'))

@bp.route('/users/remove/<user>')
@login_required
def users_remove(user):
    user = User.query.filter_by(name=user).first()
    if user in current_user.user_following:
        flash("User unfollowed successfully", "info")
        current_user.unfollow(user)
        return redirect(url_for('users.users'))
    else:
        flash(f"You are already not following {user.name}", "warning")
        return redirect(url_for('users.users'))

@bp.route('/users/delete/<user>')
@login_required
def users_delete(user):
    user = current_user
    db.session.delete(user)
    db.session.commit()
    flash("Your account was deleted successfully. Sorry to see you go.", "info")
    return redirect(url_for('index'))


@login.user_loader
def load_user(id):
    return User.query.get(id)
