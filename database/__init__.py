from flask import Flask
from flask import g
from flask_sqlalchemy import SQLAlchemy
from os import getenv


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

    from . import database_filler
    with app.app_context():
        database_filler.fill_database(app)

    return app
