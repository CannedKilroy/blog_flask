# For creating the database and defining schema
# Note sqlalchemy uses snakecase, so the actual table name
# would be something like user

from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa 
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

@login.user_loader # Register with Flask-Login
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    username: so.Mapped[str] = so.mapped_column(
        sa.String(230),
        index=True,
        unique=True)

    email: so.Mapped[str] = so.mapped_column(
        sa.String(120),
        index=True,
        unique=True)
    
    # Optional to make it nullable
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256))
    
    # write only mapped defines posts as a collection type with Post objects inside
    posts: so.WriteOnlyMapped['Post'] = so.relationship(
    back_populates='author')

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    
    ##################################################################
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.Text)
    tag: so.Mapped[str] = so.mapped_column(sa.String(length=64))
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True,
        default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.id),
        index=True
    )
    
    # so.relationship is not a real relationship but a high level view between post and author
    # it establishes a bidirectional relationship
    # posts references the 'posts' relationship in the User class ie the other side so sqlalchemy
    # knows which attributes to reference. 
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<id:{self.id} title:{self.title} tag:{self.tag} body:{self.body} timestamp:{self.timestamp} user_id:{self.user_id}>'


class Resume(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.Text)

    about_me: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    education: so.Mapped[str] = so.mapped_column(sa.Text)
    skills: so.Mapped[str] = so.mapped_column(sa.Text)
    languages: so.Mapped[str] = so.mapped_column(sa.Text)
    projects: so.Mapped[str] = so.mapped_column(sa.Text)
    experience: so.Mapped[str] = so.mapped_column(sa.Text)

    location: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    email: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    phone_num: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    linkedin: so.Mapped[str] = so.mapped_column(sa.Text)
    github: so.Mapped[str] = so.mapped_column(sa.Text)

    def __repr__(self):
        return f'<name: {self.name}, about_me: {self.about_me}, education: {self.education}...>'