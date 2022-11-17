from flask import Flask
from flask import current_app, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from database import *
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")

with app.app_context():
    # create_database(app)
    # create_tables(app)
    # empty_tables(app)
    fill_database(app)

# app.config  works

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user is None:
        return render_template("index.html", name_not_exist = True)
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return render_template("main_menu.html")
        else:
            return render_template("index.html", incorrect_password = True)


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new_account")
def new_account():
    return render_template("new_account.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    sql = "SELECT name FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user is not None:
        return render_template("new_account.html", username_taken = True)

    if len(username) < 4:
        return render_template("new_account.html", short_username = True)
    
    if len(password1) < 4:
        return render_template("new_account.html", short_password = True)

    if password1 == password2:
        password1 = generate_password_hash(password1)
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(sql, {"name":username, "password":password1})
        db.session.commit()
        # Todo 
        # Update database with user's skills etc here
        # 
        return render_template("index.html", account_created = True)
    else:
        return render_template("new_account.html", passwords_non_matching = True)