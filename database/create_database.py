import time
import psycopg2
from getpass import getpass
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import current_app

database_user = 'idlescapetester'
database_name = 'idlescapetestdb'
user_password = 'tsoha'

def new_database():
    terminal_scroll(2)
    print("(FIRST RUN) Initializes test setup with database and user.")
    sleep()
    print("(1) If database already exists")
    sleep()
    answer = input("(FIRST RUN/1)?: ")

    if answer == "1":
        return False
    elif answer == 'FIRST RUN':
        terminal_scroll(2)
        print("Enter your postgres password")
        sleep()
        print("(This is to create a database for testing and a user for it)")
        sleep()
        typed_password = getpass()
        connection = psycopg2.connect(
            database = "postgres", user="postgres", password=typed_password, host="127.0.0.1", port="5432"
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        sql_create_user = "CREATE USER " + database_user + " WITH PASSWORD '" + user_password + "' CREATEDB;"
        try:
            cursor.execute(sql_create_user)
            terminal_scroll(2)
            print("Database user '" + database_user + "' created with password '" + user_password +"'")
            sleep()
        except psycopg2.Error:
            terminal_scroll(2)
            print("User '" + database_user + "' already exists!")

        sql_create_database = "CREATE DATABASE " + database_name + " WITH OWNER " + database_user + ";"
        try:
            cursor.execute(sql_create_database)
            print("Database named '" + database_name + "' created with owner '" + database_user + "' assigned to it")
        except psycopg2.Error:
            print("Database with name '" + database_name +"' already exists!")
            terminal_scroll(2)

        cursor.close()
        return True

def create_tables():
    answer = input("Create new tables from schema.sql file? (Y/n): ")
    if answer == "n":
        return
    elif answer == "Y":
        sleep()
        print("Creating new tables from schema.sql...")
        sleep()

        with current_app.open_resource('schema.sql', mode='r') as sql_file:
            db.session.execute(sql_file.read())
        db.session.commit()
        print("Tables created! (Or they already exist)")
        terminal_scroll(2)
        

def delete_tables():
    terminal_scroll(2)
    answer = input("Do you wish to delete all tables? (YES/n): ")
    if answer == "n":
        return
    elif answer == "YES":
        db.session.execute("DROP TABLE activity_skill")
        db.session.commit()
        db.session.execute("DROP TABLE user_activity")
        db.session.commit()
        db.session.execute("DROP TABLE user_skills")
        db.session.commit()
        db.session.execute("DROP TABLE activities")
        db.session.commit()
        db.session.execute("DROP TABLE skills")
        db.session.commit()
        db.session.execute("DROP TABLE users")
        db.session.commit()
        sleep()
        print("All tables dropped!\n")
        sleep()

def terminal_scroll(length):
    if length := 2:
        sleep()
        print("")
        sleep()
        print("")
        sleep()
    elif length :=1:
        sleep()
        print("")

def sleep():
    time.sleep(0.1)