from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from config import Config

db = SQLAlchemy()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app