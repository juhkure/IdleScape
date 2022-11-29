from database.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from datetime import datetime

# Successful account creation returns 5
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
        # Save account with hashed password
        password1 = generate_password_hash(password1)
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(sql, {"name":username, "password":password1})
        db.session.commit()

        # Get user's ID
        sql = "SELECT id FROM users WHERE name=:username"
        result = db.session.execute(sql, {"username":username})
        user_id = result.fetchone()[0]

        # Add skills for user
        result = db.session.execute("SELECT name FROM skills")
        skills = result.fetchall()
        for skill in skills:
            sql = "INSERT INTO user_skills "\
                  "(user_id, skill_name, level, experience) "\
                  "VALUES (:user_id, :skill_name, :level, :experience)"
            db.session.execute(sql, {"user_id":user_id, "skill_name":skill[0], "level":int(1), "experience":int(1)})
            db.session.commit()

        # Add activities for user
        result = db.session.execute("SELECT name FROM activities")
        activities = result.fetchall()
        for activity in activities:
            sql = "INSERT INTO user_activity "\
                  "(user_id, activity_name, action_at, active) "\
                  "VALUES (:user_id, :activity_name, :action_at, :active)"
            db.session.execute(sql, {"user_id":user_id, "activity_name":activity[0], "action_at":datetime.now(), "active":False})
            db.session.commit()
        return 5

def set_activity(activity):
    user_id = session["user_id"]

    if not reward_activity():  # No currently active activity found
        print("No experience rewarded this time yet...")
    else:
        print("Experience rewarded!")

    sql = "UPDATE user_activity SET active=:active, action_at=:current_time WHERE user_id=:user_id AND activity_name=:activity"
    db.session.execute(sql, {"active":True, "current_time":datetime.now(), "user_id":user_id, "activity":activity})
    db.session.commit()

# Rewards user with accumulated experience if active activity found
def reward_activity():
    user_id = session["user_id"]
    now = datetime.now()
    sql = "SELECT user_id, activity_name, action_at FROM user_activity WHERE user_id=:user_id AND active"
    result = db.session.execute(sql, {"user_id":user_id})
    user_activity = result.fetchone()

    if user_activity is not None:
        passed_time = now - user_activity.action_at
        passed_time_in_seconds = passed_time.total_seconds()

        sql2 = "SELECT activity_name, skill_name, base_xp FROM activity_skill WHERE activity_name=:activity"
        activity_skills = db.session.execute(sql2, {"activity":user_activity.activity_name} )

        # Calculate experience earned for all skills, then insert it to user_skills
        for activity_skill in activity_skills:
            gained_xp = (passed_time_in_seconds / 100 ) * activity_skill.base_xp

            xp_insert_sql = "UPDATE user_skills SET experience = experience + :gained_xp WHERE user_id=:user_id AND skill_name=:skill"
            db.session.execute(xp_insert_sql, {"gained_xp":gained_xp, "user_id":user_id, "skill":activity_skill.skill_name})
            db.session.commit()
        
        # Set user_activity back to False
        update_user_activity = "UPDATE user_activity SET active = False WHERE user_id=:user_id AND activity_name=:activity"
        db.session.execute(update_user_activity, {"user_id":user_id, "activity":user_activity.activity_name})
        db.session.commit()
        return True
    else:
        return False

# Succesful login returns 2
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
            session["user_id"] = user.id
            return 2
        else:
            return 3

def logout():
    del session["username"]
    del session["user_id"]