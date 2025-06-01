import os
from app.exceptions import MissingEnviromentVariable

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    try:
        SECRET_KEY = os.environ['SECRET_KEY']
        SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI'] or \
            'sqlite:///' + os.path.join(base_dir, 'app.db')
        BLOG_USERNAME = os.environ.get('BLOG_USERNAME')
    except KeyError as e:
        raise MissingEnviromentVariable("Enviroment Variable Does not exist")