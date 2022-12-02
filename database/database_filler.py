from .db import db

def fill_database():
    answer = input("Do you want to fill database? (y/n): ")
    if answer == "n":
        return
    elif answer == "y":
        print("ok")
        db.session.execute("BEGIN")
        insert_activities()
        insert_skills()
        db.session.execute("COMMIT")
        print("activities and skills added!")

        db.session.execute("BEGIN")
        insert_activity_skill()
        db.session.execute("COMMIT")
        print("activity_skills added!")

def insert_activities():
    db.session.execute("INSERT INTO activities (name) VALUES ('fishing')")
    db.session.execute("INSERT INTO activities (name) VALUES ('parkour')")
    db.session.execute("INSERT INTO activities (name) VALUES ('combat (accurate)')")
    db.session.execute("INSERT INTO activities (name) VALUES ('combat (aggressive)')")
    db.session.execute("INSERT INTO activities (name) VALUES ('combat (defensive)')")
    db.session.execute("INSERT INTO activities (name) VALUES ('pray')")
    db.session.execute("INSERT INTO activities (name) VALUES ('thieve')")

def insert_skills():
    db.session.execute("INSERT INTO skills (name) VALUES ('attack')")
    db.session.execute("INSERT INTO skills (name) VALUES ('hitpoints')")
    db.session.execute("INSERT INTO skills (name) VALUES ('fishing')")
    db.session.execute("INSERT INTO skills (name) VALUES ('agility')")
    db.session.execute("INSERT INTO skills (name) VALUES ('prayer')")
    db.session.execute("INSERT INTO skills (name) VALUES ('defence')")
    db.session.execute("INSERT INTO skills (name) VALUES ('strength')")
    db.session.execute("INSERT INTO skills (name) VALUES ('thieve')")
    
    

def insert_activity_skill():
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (accurate)', 'attack', 75)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (accurate)', 'hitpoints', 25)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (aggressive)', 'strength', 75)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (aggressive)', 'hitpoints', 25)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (defensive)', 'defence', 75)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (defensive)', 'hitpoints', 25)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('fishing', 'fishing', 100)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('parkour', 'agility', 100)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('pray', 'prayer', 100)")
    db.session.execute("INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('thieve', 'thieving', 100)")

def empty_tables():
    answer = input("Empty tables?: (Y/n): ")
    if answer == "n":
        return
    elif answer == "Y":
        db.session.execute("DELETE FROM activity_skill")
        db.session.execute("DELETE FROM activities")
        db.session.execute("DELETE FROM skills")
        db.session.execute("DELETE FROM user_activity")
        db.session.execute("DELETE FROM user_skills")
        db.session.execute("DELETE FROM users")
        db.session.commit()