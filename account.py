from database.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from datetime import datetime
import math

# Successful account creation returns 5
def create(username, password1, password2):
    sql = "SELECT name FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username": username})
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
        db.session.execute(sql, {"name": username, "password": password1})
        db.session.commit()

        # Get user's ID
        sql = "SELECT id FROM users WHERE name=:username"
        result = db.session.execute(sql, {"username": username})
        user_id = result.fetchone()[0]

        # Add skills for user
        result = db.session.execute("SELECT name FROM skills")
        skills = result.fetchall()
        for skill in skills:
            sql = "INSERT INTO user_skills "\
                  "(user_id, skill_name, level, experience, current_level_xp, experience_left) "\
                  "VALUES (:user_id, :skill_name, :level, :experience, :current_level_xp, :experience_left)"
            db.session.execute(sql, {"user_id": user_id, "skill_name": skill[0], "level": int(
                1), "experience": int(0),"current_level_xp": int(0),  "experience_left": int(83)})
            db.session.commit()

        # Add activities for user
        result = db.session.execute("SELECT name FROM activities")
        activities = result.fetchall()
        for activity in activities:
            sql = "INSERT INTO user_activity "\
                  "(user_id, activity_name, action_at, active) "\
                  "VALUES (:user_id, :activity_name, :action_at, :active)"
            db.session.execute(sql, {
                  "user_id": user_id, 
                  "activity_name": activity[0], 
                  "action_at": datetime.now(), 
                  "active": False})
            db.session.commit()
        return 5


def set_activity(activity):
    user_id = session["user_id"]
    current_activity = reward_user()

    if current_activity == activity:
        print("Experience rewarded!")
    elif current_activity is None:  # No currently active activity found
        sql = "UPDATE user_activity SET active=:active, action_at=:current_time WHERE user_id=:user_id AND activity_name=:activity"
        db.session.execute(sql, {"active": True, "current_time": datetime.now(), "user_id": user_id, "activity": activity})
        db.session.commit()
    else: # Current activity wasn't the same as chosen with set_activity()
        sql = "UPDATE user_activity SET active=:active WHERE user_id=:user_id AND activity_name=:activity"
        db.session.execute(sql, {"active":False, "user_id":user_id, "activity":current_activity})
        sql = "UPDATE user_activity SET active=:active, action_at=:current_time WHERE user_id=:user_id AND activity_name=:activity"
        db.session.execute(sql, {"active":True, "current_time":datetime.now(), "user_id":user_id, "activity":activity})
        db.session.commit()


def get_activity():
    user_id = session["user_id"]

    sql = "SELECT activity_name FROM user_activity WHERE user_id=:user_id AND active"
    result = db.session.execute(sql, {"user_id": user_id})
    user_activity = result.fetchone()

    if user_activity is not None:
        activity = user_activity.activity_name
    else:
        activity = None

    return activity


def get_active_skills(activity):
    sql = "SELECT skill_name FROM activity_skill WHERE activity_name=:activity"
    result = db.session.execute(sql, {"activity": activity})
    skills = result.fetchall()

    return skills

# Rewards user with accumulated experience if active activity found
def reward_user():
    user_id = session["user_id"]
    sql = "SELECT user_id, activity_name, action_at FROM user_activity WHERE user_id=:user_id AND active"
    result = db.session.execute(sql, {"user_id": user_id})
    user_activity = result.fetchone()

    if user_activity is None:
        return None  # No active activity

    reward_activity(user_activity.activity_name, user_activity.action_at)
            
    sql = "UPDATE user_activity SET action_at=:current_time " \
          "WHERE user_id=:user_id AND activity_name=:activity"
    db.session.execute(sql, {"current_time": datetime.now(), "user_id": user_id, "activity": user_activity.activity_name})
    db.session.commit()

    return user_activity.activity_name  # Active activity found and xp was rewarded

def reward_activity(activity_name, past_action):
    user_id = session["user_id"]
    passed_time = passed_time_in_seconds(past_action)

    sql = "SELECT activity_name, skill_name, base_xp FROM activity_skill WHERE activity_name=:activity"
    activity_skills = db.session.execute(sql, {"activity": activity_name})

    # Calculate experience earned for all affected skills, then insert it to user_skills
    for activity_skill in activity_skills:
        sql = "SELECT experience, level, current_level_xp, experience_left " \
                "FROM user_skills WHERE user_id=:user_id AND skill_name=:name"
        user_skills = db.session.execute(sql, {"user_id": user_id, "name": activity_skill.skill_name})

        user_skills = user_skills.fetchone()
        current_xp = user_skills[0]
        current_level = user_skills[1]
        current_level_xp = user_skills[2]
        remaining_xp = user_skills[3]

        # This is to take into account users affected by database update (in production)
        if current_level_xp == -1:
            current_level_xp = current_and_next_level_experience(current_level)[0]
        if remaining_xp == 999999:
            remaining_xp = current_and_next_level_experience(current_level)[1] - current_xp

        # Experience calculation, determines speed of progression
        gained_xp = (passed_time / 100) * (activity_skill.base_xp + activity_skill.base_xp * 0.1 * (current_level - 1))

        # While loop to calculate new level
        new_xp = current_xp + gained_xp
        new_level_xp = next_level_xp(current_level, current_level_xp)
        new_level = current_level
        while new_xp >= new_level_xp:
            current_level_xp = new_level_xp  # Current_level_xp trails behind one level
            new_level += 1
            new_level_xp = next_level_xp(new_level, new_level_xp)
        remaining_xp = new_level_xp - new_xp

        update_skill(current_level, new_level, gained_xp, current_level_xp, remaining_xp, user_id, activity_skill.skill_name)
    return 1

def update_skill(current_level, new_level, gained_xp, current_level_xp, remaining_xp, user_id, skill_name):
    if new_level > current_level: # Update if level changed
        sql = "UPDATE user_skills "                                                            \
              "SET experience = experience + :gained_xp, current_level_xp=:current_level_xp, " \
                  "level=:new_level, experience_left=:remaining_xp "                           \
              "WHERE user_id=:user_id AND skill_name=:skill"
        db.session.execute(sql, {"gained_xp": gained_xp, "current_level_xp": current_level_xp, 
            "new_level": new_level, "remaining_xp": remaining_xp, "user_id": user_id, "skill": skill_name})
    else: # Update if level didn't change
        sql = "UPDATE user_skills "                                                      \
              "SET experience = experience + :gained_xp, experience_left=:remaining_xp " \
              "WHERE user_id=:user_id AND skill_name=:skill"
        db.session.execute(sql, {"gained_xp": gained_xp, "remaining_xp": remaining_xp, 
            "user_id": user_id, "skill": skill_name})
    db.session.commit()

def passed_time_in_seconds(last_action):
    passed_time = datetime.now() - last_action
    passed_time = passed_time.total_seconds()
    if passed_time > 86400:
        passed_time = 86400

    return passed_time # Returns a maximum of 24hours in seconds

def get_skill_info(skill_name):
    reward_user()

    experience_rate = 0
    total_experience = 0
    experience_till_next_level = 0
    user_id = session["user_id"]

    sql = "SELECT level, experience FROM user_skills WHERE user_id=:user_id AND skill_name=:name"
    result = db.session.execute(sql, {"user_id": user_id, "name": skill_name})
    level_and_xp = result.fetchone()
    current_level = level_and_xp[0]
    total_experience = level_and_xp[1]
    experience_till_next_level = experience_remaining(
        current_level, total_experience)

    activity = get_activity()

    if activity is not None:
        active_skills = get_active_skills(activity)
        for active_skill in active_skills:
            active_skill_name = active_skill.skill_name
            # print(active_skill.skill_name)
            # print(skill_name)
            if active_skill_name == skill_name:
                base_experience_rate = get_base_experience_rate(
                    active_skill_name, activity)
                experience_rate = calculate_experience_rate(
                    base_experience_rate, current_level)

    return current_level, total_experience, experience_rate, experience_till_next_level

# Calculates next level's experience assuming previous level's total experience is given 
def next_level_xp(current_level, current_level_experience):
    return math.floor(current_level_experience + math.floor(current_level + 300 * pow(2, current_level/7))/4)

# Returns xp requirements for level and level+1
def current_and_next_level_experience(level):
    required_xp = 0
    i = 1
    while i <= level:
        current_xp = required_xp
        required_xp += math.floor(i + 300 * pow(2, i/7))
        i += 1
    return math.floor(current_xp/4), math.floor(required_xp/4)

# Returns remaining xp for next level. True if next level achieved.
def experience_remaining(level, current_experience):
    next_level_experience = current_and_next_level_experience(level)[1]
    if current_experience < next_level_experience:
        return next_level_experience - current_experience
    else:
        return True


def get_base_experience_rate(skill, activity):
    sql = "SELECT base_xp FROM activity_skill WHERE activity_name=:activity AND skill_name=:skill"
    result = db.session.execute(sql, {"activity": activity, "skill": skill})

    return result.fetchone()[0]


def calculate_experience_rate(base_xp, level):
    return base_xp + base_xp * 0.1 * (level - 1)


def get_account_skills():
    user_id = session["user_id"]
    sql = "SELECT skill_name, level, experience_left, experience, current_level_xp FROM user_skills WHERE user_id=:user_id ORDER BY skill_name"
    result = db.session.execute(sql, {"user_id": user_id})
    skills = result.fetchall()

    return skills

# Succesful login returns 2
def login(username, password):
    sql = "SELECT id, password FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return 1
        
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
