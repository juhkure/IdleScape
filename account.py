from database.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from datetime import datetime
import math

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

def get_activity():
    user_id = session["user_id"]
    
    sql = "SELECT activity_name FROM user_activity WHERE user_id=:user_id AND active"
    result = db.session.execute(sql, {"user_id":user_id})
    user_activity = result.fetchone()

    if user_activity is not None:
        activity = user_activity.activity_name
    else:
        activity = None

    return activity

def get_active_skills(activity):
    sql = "SELECT skill_name FROM activity_skill WHERE activity_name=:activity"
    result = db.session.execute(sql, {"activity":activity})
    skills = result.fetchall()

    return skills

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
            current_xp_sql = "SELECT experience, level FROM user_skills WHERE user_id=:user_id AND skill_name=:name"
            result = db.session.execute(current_xp_sql, {"user_id":user_id, "name":activity_skill.skill_name})

            xp_and_level = result.fetchone()
            current_xp = xp_and_level[0]
            current_level = xp_and_level[1]

            # Experience calculation, determines speed of progression
            gained_xp = (passed_time_in_seconds / 100 ) * (activity_skill.base_xp + activity_skill.base_xp * 0.1 * (current_level -1))

            new_xp = current_xp + gained_xp
            # Calculate new level based on new_xp
            new_level = 0
            required_xp = 0
            for i in range(1,99):
                required_xp += math.floor(i + 300 * pow(2, i/7))
                if new_xp < (math.floor(required_xp/4)):
                    new_level = i
                    break
            
            if (new_level > current_level):
                xp_insert_sql = "UPDATE user_skills SET experience = experience + :gained_xp, level=:new_level WHERE user_id=:user_id AND skill_name=:skill"
                db.session.execute(xp_insert_sql, {"gained_xp":gained_xp, "new_level":new_level, "user_id":user_id, "skill":activity_skill.skill_name})
            else:
                xp_insert_sql = "UPDATE user_skills SET experience = experience + :gained_xp WHERE user_id=:user_id AND skill_name=:skill"
                db.session.execute(xp_insert_sql, {"gained_xp":gained_xp, "user_id":user_id, "skill":activity_skill.skill_name})
            db.session.commit()

        # Set user_activity back to False
        update_user_activity = "UPDATE user_activity SET active = False WHERE user_id=:user_id AND activity_name=:activity"
        db.session.execute(update_user_activity, {"user_id":user_id, "activity":user_activity.activity_name})
        db.session.commit()
        return True # Active activity found and xp was rewarded
    else:
        return False # No active activity

def get_skill_info(skill_name):
    experience_rate = 0
    total_experience = 0
    user_id = session["user_id"]

    sql = "SELECT level, experience FROM user_skills WHERE user_id=:user_id AND skill_name=:name"
    result = db.session.execute(sql, {"user_id":user_id, "name":skill_name})
    level_and_xp = result.fetchone()
    current_level = level_and_xp[0]
    total_experience = level_and_xp[1]

    activity = get_activity()

    if activity is not None:
        active_skills = get_active_skills(activity)
        for active_skill in active_skills:
            active_skill_name = active_skill.skill_name
            # print(active_skill.skill_name)
            # print(skill_name)
            if active_skill_name == skill_name:
                base_experience_rate = get_base_experience_rate(active_skill_name, activity)
                experience_rate = calculate_experience_rate(base_experience_rate, current_level)



    

    return current_level, total_experience, experience_rate

def get_base_experience_rate(skill, activity):
    sql = "SELECT base_xp FROM activity_skill WHERE activity_name=:activity AND skill_name=:skill"
    result = db.session.execute(sql, {"activity":activity, "skill":skill})

    return result.fetchone()[0]

def calculate_experience_rate(base_xp, level):
    return base_xp + base_xp * 0.1 * (level -1)

def get_account_skills():
    user_id = session["user_id"]
    sql = "SELECT skill_name, level, experience FROM user_skills WHERE user_id=:user_id ORDER BY skill_name"
    result = db.session.execute(sql, {"user_id":user_id})

    return result

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