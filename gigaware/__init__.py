import os
from gigaware.config import config_env_files
from flask import Flask

from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from gigaware.models import init_models_module
from gigaware import translator

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name='development', p_db=db, p_bcrypt=bcrypt, p_login_manager=login_manager):
    new_app = Flask(__name__)
    config_app(config_name, new_app)

    p_db.init_app(new_app)
    p_bcrypt.init_app(new_app)
    p_login_manager.init_app(new_app)
    p_login_manager.login_view = 'register'
    db.init_app(new_app)
    init_models_module(db, p_bcrypt, new_app)

    # Add translator utilities.
    new_app.add_template_global(translator.translate)

    return new_app

def config_app(config_name, new_app):
    new_app.config.from_object(config_env_files[config_name])

app = create_app()

import gigaware.views