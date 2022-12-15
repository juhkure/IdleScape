from app import app
import account
from flask import render_template, jsonify, request, session, redirect, flash, abort
import secrets



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main_menu")
def main_menu():
    skills = account.get_account_skills()

    return render_template("main_menu.html", skills=skills)

# Also updates the progress to the skill
@app.route("/skill_info", methods=["POST"])
def experience_rate():
    skill_name = request.json['name']
    info = account.get_skill_info(skill_name)

    current_level = info[0]
    total_experience = info[1]
    experience_rate = info[2]
    experience_left = info[3]

    return jsonify({'currentLevel':current_level, 'totalExperience':total_experience, 'experienceRate':experience_rate, 'experienceLeft':experience_left})

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["csrf_token"] = secrets.token_hex(16)

    confirmation = account.login(username, password)
    if confirmation == 1: # User not found
        return render_template("index.html", name_not_exist = True)

    if confirmation == 2: # Success!
            return redirect("/main_menu")

    if confirmation == 3: # Incorrect password
            return render_template("index.html", incorrect_password = True)

@app.route("/logout")
def logout():
    del session["csrf_token"]
    
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
    if confirmation == 1: # Name taken
        return render_template("new_account.html", username_taken = True)

    if confirmation == 2: # Short name
        return render_template("new_account.html", short_username = True)

    if confirmation == 3: # Short password
        return render_template("new_account.html", short_password = True)

    if confirmation == 4: # Passwords don't match
        return render_template("new_account.html", passwords_non_matching = True)
        
    if confirmation == 5: # Success!
        return render_template("index.html", account_created = True)

@app.route("/set_activity", methods=["POST"])
def set_activity():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    activity = request.form["activity"]
    if activity != "not selected":
        account.set_activity(activity)
        flash(activity, "activity")
    else:
        flash("Activity not selected!", "error")

    return redirect("/main_menu")

    # Todo fetch selected activity and assign it to user
