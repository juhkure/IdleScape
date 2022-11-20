from flask import Flask
from flask import current_app, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv

app = Flask(__name__)

import routes



# import database

# with app.app_context():
#     database.create_tables(app)
#     database.empty_tables(app)
#     database.fill_database(app)
