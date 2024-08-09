# Flask-WTF uses classes to represent web forms, with the fields represented
# as variables
# Fields that are defined in the loginform class know how to render themselves
# as html 

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User
from flask_mdeditor import MDEditorField


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label = 'Sign In')


# Form to register as new user
class RegistrationForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired()]
        )

    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()]
    )

    # Password and confirm password
    password = PasswordField(
        label='Password',
        validators=[DataRequired()]
        )
    password2 = PasswordField(
        label='Confirm Password',
        validators=[DataRequired(), EqualTo(fieldname='password')]
        )
    submit = SubmitField(label='Submit')
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me')
    new_password = PasswordField('New Password')
    new_password2 = PasswordField(
        'Repeat Password',
        validators=[EqualTo('new_password', message='Passwords must match')]
        )
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        # Pass in original username, which is current user
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        # If new username is different from the original
        # Check username is unique
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username. This one is taken')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    body = MDEditorField('Content', validators=[DataRequired()])
    delete = BooleanField('Delete this post') 
    submit = SubmitField('Submit')

class ResumeForm(FlaskForm):
    # DO NOT USE MDEDITORFIELD HERE, IT DOES NOT WORK HERE IDK WHY
    name = TextAreaField('name')
    about_me = TextAreaField('about_me')
    education = TextAreaField('education')
    skills = TextAreaField('skills')
    languages = TextAreaField('languages')
    projects = TextAreaField('projects')
    experience = TextAreaField('experience')
    location = TextAreaField('location')
    email = TextAreaField('email')
    phone_num = TextAreaField('phone_num')
    linkedin = TextAreaField('linkedin')
    github = TextAreaField('github')

    submit = SubmitField('Submit')
