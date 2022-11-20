from app import app
import account
from flask import render_template, request, session, redirect



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    confirmation = account.login(username, password)

    if confirmation == 1:
        return render_template("index.html", name_not_exist = True)
    if confirmation == 2:
            return render_template("main_menu.html")
    if confirmation == 3:
            return render_template("index.html", incorrect_password = True)

@app.route("/logout")
def logout():
    account.logout()
    return redirect("/")

@app.route("/new_account")
def new_account():
    return render_template("new_account.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    confirmation = account.create(username, password1, password2)
    if confirmation == 1:
        return render_template("new_account.html", username_taken = True)
    if confirmation == 2:
        return render_template("new_account.html", short_username = True)
    if confirmation == 3:
        return render_template("new_account.html", short_password = True)
    if confirmation == 4:
        return render_template("new_account.html", passwords_non_matching = True)
    if confirmation == 5:
        return render_template("index.html", account_created = True)

@app.route("/update_activity", methods=["POST"])
def update_activity():

    return