from app import app, run_mode
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from database import *

created_new = False

# Initial configuration according to run_mode
if run_mode == 0:
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.secret_key = getenv("SECRET_KEY")
else:
    if run_mode == 1:
        from .create_database import new_database
        created_new = new_database()
    test_database_url = "postgresql://" + dbuser + ":" + dbuser_pw + "@/" + dbname
    app.config["SQLALCHEMY_DATABASE_URI"] = test_database_url
    app.secret_key = "12345qwertasdfgzxcvb6789yuiohjkl"
    

db = SQLAlchemy(app)


if run_mode == 1 or run_mode == 2:
    from .create_database import delete_tables, create_tables
    with app.app_context():
        if not created_new or run_mode == 2:
            delete_tables()
        create_tables()

        from .database_filler import *
        if not created_new or run_mode == 2:
            empty_tables()
        fill_database()