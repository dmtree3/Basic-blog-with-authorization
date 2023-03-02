from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db, mail
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm, LoginForm, ChangePasswordForm, ChangeUsernameForm, PasswordResetForm, RequestResetForm
from flask_mail import Message

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash('Logged in successfully', category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Password', category='error')
        else:
            flash('Email is not registered', category='error')
    return render_template("login.html", title='Login', user=current_user, form=form)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', category='success')
        return redirect(url_for('auth.login'))
    return render_template("sign-up.html", title='Sign Up', user=current_user, form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_hashed_password = generate_password_hash(form.new_password.data, method='sha256')
        current_user.password = new_hashed_password
        db.session.commit()
        flash('Password updated!', category='success')
        return redirect(url_for('views.home'))
    return render_template('change-password.html', form=form, user=current_user, title='Change Password')


@auth.route("/change-username", methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        new_username = form.new_username.data
        current_user.username = new_username
        db.session.commit()
        flash('Username updated!', category='success')
        return redirect(url_for('views.home'))
    return render_template('change-username.html', form=form, user=current_user, title='Change Username')


def send_mail(user):
    token = user.generate_reset_token()
    message = Message('Password reset', sender='noreply@dm3.com', recipients=[user.email])
    message.body = f"Follow the link to reset your password: {url_for('auth.reset_token', token=token, _external=True)}"
    mail.send(message)


@auth.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_mail(user)
        flash('Email has been sent to your address', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset-request.html', form=form, title='Request password reset', user=current_user)


@auth.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Token is invalid or expired', category='error')
        return redirect(url_for('auth.reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        new_hashed_password = generate_password_hash(form.new_password.data, method='sha256')
        current_user.password = new_hashed_password
        db.session.commit()
        flash('Password updated!', category='success')
        return redirect(url_for('views.home'))
    return render_template('reset-token.html', form=form, title='Reset password')
