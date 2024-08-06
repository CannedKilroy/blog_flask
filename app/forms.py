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
    submit = SubmitField('Submit')

class ResumeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    about_me = TextAreaField('About_Me', validators=[DataRequired()])
    education = TextAreaField('education', validators=[DataRequired()])
    skills = TextAreaField('skills', validators=[DataRequired()])
    languages = TextAreaField('languages', validators=[DataRequired()])
    projects = TextAreaField('projects', validators=[DataRequired()])
    experience = TextAreaField('experience', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    email = StringField('email')
    phone_num = StringField('phone_num')
    linkedin = StringField('linkedin', validators=[DataRequired()])
    github = StringField('github', validators=[DataRequired()])