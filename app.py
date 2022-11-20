import database
from flask import Flask
from flask import current_app, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime



init_type = input("Select use case: (1) Local testing/development or (2) Production?: ")
if init_type == "1":
    created_new = database.new_database()
    test_database_url = ("postgresql://" + database.database_user + ":" + database.user_password + "@/" + database.database_name + "")

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = test_database_url
    app.secret_key = "12345qwertasdfgzxcvb6789yuiohjkl"
    if not created_new:
        with app.app_context():
            database.delete_tables(app)
elif init_type == "2":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.secret_key = getenv("SECRET_KEY")



with app.app_context():
    database.create_tables(app)
    database.empty_tables(app)
    database.fill_database(app)

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

    if password1 != password2:
        return render_template("new_account.html", passwords_non_matching = True)
    else:
        password1 = generate_password_hash(password1)
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(sql, {"name":username, "password":password1})
        db.session.commit()

        sql = "SELECT id FROM users WHERE name=:username"
        result = db.session.execute(sql, {"username":username})
        user_id = result.fetchone()[0]

        result = db.session.execute("SELECT name FROM skills")
        skills = result.fetchall()
        for skill in skills:
            sql = "INSERT INTO user_skills "\
                  "(user_id, skill_name, level, experience) "\
                  "VALUES (:user_id, :skill_name, :level, :experience)"
            db.session.execute(sql, {"user_id":user_id, "skill_name":skill[0], "level":int(1), "experience":int(1)})
            db.session.commit()

        result = db.session.execute("SELECT name FROM activities")
        activities = result.fetchall()
        for activity in activities:
            sql = "INSERT INTO user_activity "\
                  "(user_id, activity_name, action_at, active) "\
                  "VALUES (:user_id, :activity_name, :action_at, :active)"
            db.session.execute(sql, {"user_id":user_id, "activity_name":activity[0], "action_at":datetime.now(), "active":False})
            db.session.commit()

        return render_template("index.html", account_created = True)

@app.route("/update_activity", methods=["POST"])
def update_activity():
    
    return