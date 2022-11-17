from website import create_app
from flask import Flask
from flask import current_app
from flask import g
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = create_app()

# app.config  works

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_account")
def create_account():
    return render_template("create_account.html")