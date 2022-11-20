from flask_sqlalchemy import SQLAlchemy
from flask import current_app


def fill_database(app):
    answer = input("Do you want to fill database? (y/n): ")
    if answer == "n":
        return
    elif answer == "y":
        db = SQLAlchemy(app)
        print("ok")
        db.session.execute("BEGIN")
        insert_activities(db)
        insert_skills(db)
        db.session.execute("COMMIT")
        print("activities and skills added!")

        db.session.execute("BEGIN")
        insert_activity_skill(db)
        db.session.execute("COMMIT")
        print("activity_skills added!")


def insert_activities(database):
    database.session.execute("INSERT INTO activities (name) VALUES ('combat')")
    database.session.execute("INSERT INTO activities (name) VALUES ('fishing')")
    database.session.execute("INSERT INTO activities (name) VALUES ('parkour')")
    database.session.execute("INSERT INTO activities (name) VALUES ('pray')")

def insert_skills(database):
    database.session.execute("INSERT INTO skills (name) VALUES ('attack')")
    database.session.execute("INSERT INTO skills (name) VALUES ('hitpoints')")
    database.session.execute("INSERT INTO skills (name) VALUES ('fishing')")
    database.session.execute("INSERT INTO skills (name) VALUES ('agility')")
    database.session.execute("INSERT INTO skills (name) VALUES ('prayer')")

def insert_activity_skill(database):
    database.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat', 'attack', 75)")
    database.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat', 'hitpoints', 25)")
    database.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('fishing', 'fishing', 100)")
    database.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('parkour', 'agility', 100)")
    database.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('pray', 'prayer', 100)")


def empty_tables(app):
    answer = input("Empty tables?: (Y/n): ")
    if answer == "n":
        return
    elif answer == "Y":
        db = SQLAlchemy(current_app)
        db.session.execute("DELETE FROM activity_skill")
        db.session.execute("DELETE FROM activities")
        db.session.execute("DELETE FROM skills")
        db.session.execute("DELETE FROM user_activity")
        db.session.execute("DELETE FROM user_skills")
        db.session.execute("DELETE FROM users")
        db.session.commit()