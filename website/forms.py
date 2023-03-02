from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, ValidationError, TextAreaField, SubmitField
from wtforms.validators import EqualTo, Email, DataRequired, Length
from .models import User
from flask import flash


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        email_exists = User.query.filter_by(email=email.data).first()
        if email_exists:
            flash('Email is already taken', category='error')
            raise ValidationError('Email is already taken')

    def validate_username(self, username):
        username_exists = User.query.filter_by(username=username.data).first()
        if username_exists:
            flash('Username is already taken', category='error')
            raise ValidationError('Username is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Submit')


class ChangeUsernameForm(FlaskForm):
    new_username = StringField('New Username', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Submit')

    def validate_new_username(self, new_username):
        username_exists = User.query.filter_by(username=new_username.data).first()
        if username_exists:
            flash('Username is already taken', category='error')
            raise ValidationError('Username is already taken')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reqeust password reset')

    def validate_email(self, email):
        email_exists = User.query.filter_by(email=email.data).first()
        if not email_exists:
            flash('Email you typed is not registered', category='error')
            raise ValidationError('Email you typed is not registered')


class PasswordResetForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset password')

