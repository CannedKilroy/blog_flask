from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mdeditor import MDEditor
from logging.handlers import RotatingFileHandler

import logging
import os
import markdown2

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config) # Read and apply the configs
db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)
app.config['MDEDITOR_FILE_UPLOADER'] = os.path.join(basedir, 'static', 'images')
mdeditor = MDEditor(app)

# Define a custom filter to convert Markdown to HTML
@app.template_filter('markdown')
def markdown_to_html(markdown_text):
    """Convert Markdown text to HTML"""
    html = markdown2.markdown(markdown_text)
    return html

app.jinja_env.filters['markdown'] = markdown_to_html

# If non logged in user tries view protected page,
# redirect to login form, and then direct them back
# to the original page once verified
login = LoginManager(app)
login.login_view = 'login'

if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors
