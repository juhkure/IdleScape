from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from .database_filler import fill_database, empty_tables
from .create_database import new_database, create_tables, user_password, database_user, database_name, delete_tables


init_type = input("Select use case: (1) Local testing/development or (2) Production?: ")
if init_type == "1":
    created_new = new_database()
    test_database_url = ("postgresql://" + database_user + ":" + user_password + "@/" + database_name + "")

    app.config["SQLALCHEMY_DATABASE_URI"] = test_database_url
    app.secret_key = "12345qwertasdfgzxcvb6789yuiohjkl"
    if not created_new:
        with app.app_context():
            delete_tables(app)
elif init_type == "2":
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)

__all__ = [
    'fill_database',
    'empty_tables'
    'new_database', 
    'create_tables', 
    'user_password',
    'database_user',
    'database_name',
    'delete_tables'
]