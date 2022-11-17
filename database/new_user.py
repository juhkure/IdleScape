from flask_sqlalchemy import SQLAlchemy

def create_user(app, name):
    db = SQLAlchemy(app)

    # result1 = db.session.execute("SELECT id FROM users WHERE name= {name}")
    sql = "SELECT id FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":name})
    user_id = result.fetchone()[0]

    db.session.execute("BEGIN")
    insert_user_skills(db, name, user_id)
    db.session.execute("COMMIT")

    return

def insert_user_skills(database, name, id):
    # Search for all skills in database, and for each make user_skills for user
    
    database.session.execute("INSERT INTO user_skills (")
