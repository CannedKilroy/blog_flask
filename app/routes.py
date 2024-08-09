from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResumeForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Resume, Post
import sqlalchemy as sa
from datetime import datetime, timezone
from flask import current_app
from werkzeug.security import generate_password_hash

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

When the browser sends the POST request when 
the user presses on the submit button
it will gather the data and run the validators 
and return true if the data is valid

db.session for simple crud operations
'''


'''
Index ie home page
'''
@app.route('/')
@app.route('/index')
def index():
    # Get the user object
    # Returns None if no rows present
    username = current_app.config['BLOG_USERNAME']
    user = db.first_or_404(sa.select(User).where(User.username == username))
    if user is None:
        flash('User does not exist')
    posts = db.session.scalars(
        sa.select(Post).order_by(Post.timestamp.desc())).all()
    
    result = db.session.execute(sa.select(Resume).where(Resume.id == 1))
    resume = result.scalar_one_or_none()
    
    return render_template('index.html', user=user, posts=posts, resume=resume)


'''
Login url
Not shown on website
Manually navigate to url
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Login', form=form)


"""
Logout User
"""
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


"""
Register User
"""
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


"""
User Profile
"""
@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = db.session.scalars(
        sa.select(Post).order_by(Post.timestamp.desc())).all()
    return render_template('user.html', user=user, posts=posts)


"""
Edit user profile
"""
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        if form.new_password.data:
            current_user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()





"""
Explore Blog Posts
"""
@app.route('/blog')
def blog():
    username = current_app.config['BLOG_USERNAME']
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = db.session.scalars(sa.select(Post).order_by(Post.timestamp.desc())).all()
    return render_template("explore.html", title='Explore', posts=posts)


"""
Create / Edit Posts
"""
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@app.route('/create_post', defaults={'post_id': None}, methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()

    if post_id:
        title = 'Edit Post'
        post = Post.query.get_or_404(post_id)
    else:
        title = 'Create Post'
        post = Post()
        post.user_id = current_user.id
    
    # Populate fields
    if request.method == 'GET' and post_id:
        form.title.data = post.title
        form.body.data = post.body
        form.tag.data = post.tag

    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(post)
            db.session.commit()
            flash('Post has been deleted.')
            return redirect(url_for('index'))
        else:
            post.title = form.title.data
            post.body = form.body.data
            post.tag = form.tag.data
            # If new post, add to session
            if not post_id:
                db.session.add(post)
            db.session.commit()
            flash('Your post has been published!' if not post_id else 'Your post has been updated!')
            return redirect(url_for('index'))
    return render_template('post_form.html', title=title, form=form, post_id=post_id)


"""
Render post
"""
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

"""
Render Resume
"""
@app.route('/resume')
def resume():
    result = db.session.execute(sa.select(Resume).where(Resume.id == 1))
    resume = result.scalar_one_or_none()
    return render_template('resume.html', title='Resume', resume=resume)

"""
Edit resume
"""
@app.route('/edit_resume/<int:resume_id>', methods=['GET', 'POST'])
@login_required
def edit_resume(resume_id=None):

    if resume_id:
        title='Edit Resume'
        resume = Resume.query.get_or_404(resume_id)
        msg = 'Your resume has been updated!'
    else:
        title='Create Resume'
        resume = Resume()
        msg = 'Your resume has been Created!'
    
    # Populate form with existing info
    form = ResumeForm(obj=resume)

    if form.validate_on_submit():
        form.populate_obj(resume)
        if not resume_id:
            db.session.add(resume)
        db.session.commit()
        flash(msg)
        return redirect(url_for('index'))
    if resume_id:
        form.skills.data = resume.skills
        
    return render_template('resume_form.html', title=title, resume_id=1, form=form)