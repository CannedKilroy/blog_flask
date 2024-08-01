from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
import sqlalchemy as sa
from datetime import datetime, timezone


# Maps the urls of / and /index to this view function
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }]


    # Render_template takes the bare html, 
    # subs in the data, and returns the rendered template
    return render_template('index.html', title='Home', posts=posts)


'''
This tells flask that the view function accepts GET and POST
requests, overriding the default GET request only. GET requests 
are those that return information to the client ie web browser.
POST request are typically used when the browser submits form data
to the server.

GET requests are used to retrieve data from the server, and should
not change the state of the server, should only retrieve data.

POST requests are used to send data to the server ie create or 
update a resource. Typically used when submitting form data. 

Use the url_for so to not hardcode the links. Url_for generates
url links based on the internal mapping of urls to view functions
ie, url_for('index') returns "/login"
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    # When the browser sends the POST request when 
    # the user presses on the submit button
    # it will gather the data and run the validators 
    # and return true if the data is valid

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():

        # Get the user object
        # db.session for simple crud operations
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)

        # Since the user is logged in, get the next page
        # from the client sent with the request
        next_page = request.args.get('next')
        
        # If no next page, send to index
        # If its a relative path, send to that url
        # If next is full url that includes domain name, 
        # redirect to index (insecure if you dont)
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(message='You are registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
    {'author': user, 'body': 'Test post #1'},
    {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Resume')