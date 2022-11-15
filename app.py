from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)




answer = input("Do you want to fill database? (y/n): ")
if answer == "y":
    db.session.execute("INSERT INTO activities (id, name) VALUES (1, 'fishing')")
    db.session.commit()
    # init_db.testi()

@app.route("/")
def index():
    return render_template("index.html")