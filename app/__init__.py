import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///notes.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    else:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        from . import models, routes
        db.create_all()
        app.register_blueprint(routes.bp)

    return app
