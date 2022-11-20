from database.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from datetime import datetime


def create(username, password1, password2):
    sql = "SELECT name FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user is not None:
        return 1
    if len(username) < 4:
        return 2
    if len(password1) < 4:
        return 3
    if password1 != password2:
        return 4
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
        return 5

def login(username, password):
    sql = "SELECT id, password FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user is None:
        return 1
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return 2
        else:
            return 3

def logout():
    del session["username"]