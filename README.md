# IdleScape

Game can be tested/played [HERE!](https://idle-scape.fly.dev/)
-

A [RuneScape](https://www.runescape.com/) influenced idle/[incremental](https://en.wikipedia.org/wiki/Incremental_game) -game which's objective is very simple: level and build up your character slowly but surely with mostly inactive gameplay.

Idlescape's goal isn't to provide a highly interactive gameplay loop but rather a casual experience that allows you to attend to life's boring but obligatory tasks like work and school, all the while you're gaining progression in a game!

The game's initial page allows the user to create and log in to their character/account. Upon logging in, the main page will show them:

- Skills and their levels
- Total level and experience
- User's current chosen activity
- Experience amount that the activity produces

The player can choose an activity to log their participation in from a list of different activities. This chosen activity determines the amount of experience and the target skill this experience goes to. For example, a combat activity would reward the player with experience towards combat skills like strength and hitpoints. Or the player could choose a skilling activity like fishing to further their levels in the fishing skill.

Player's skills are considered their "stats", and each of these stats/skills start from level 1 and can be levelled up all the way to 99. Each new level will require more experience than the previous one.

## Features

Things (hopefully) working currently are:
* Ability to create a user and a database to PostgreSQL
* Add/remove tables from this database. Adding is done using [schema.sql](https://github.com/juhkure/IdleScape/blob/main/schema.sql)
* Populate these tables according to current gamedesign
* Show basic html pages for login and account creation
* Accounts can be created and used to log in.
* New account creates necessary rows in database for game logic. Password is hashed.
* User can select an active activity for their account.
* Selecting an activity rewards the account with experience in previously active activity.
* Main menu lists user's skills, levels, and experience.
* User can click a skill's image to show more info about it

### Current Main menu visuals:

![Main Menu](https://github.com/juhkure/IdleScape/blob/main/readme_images/main_menu.png)

# Plans

The current plan is to do calculations and database logic within the backend server. A small portion in "frontend" will be done with JavaScript to allow a more visual and smoother user experience. At it's core, the game's database consists of just 6 tables to track users, their skills, and their chosen activity.

Further plans consist of things like unlocks/achievements and items that allows the player to further plan and customize their progression but their implementation is for now, out of reach.

# Instructions for testing

### Testing requirements ###

* [PostgreSQL](https://www.postgresql.org/download/ "PostgreSQL download page")
* Python


## Windows

You can follow the Linux steps down below mostly the same, however there's few steps that you might want to look out for:

```
$ python3 -m venv venv
```

might or might not work, if not, try using

```
$ winpty python -m venv venv
```

Also the next step where we activate venv. For windows depending on the terminal of you're using:

```
. venv/Scripts/activate
```
or    (NOTE, there's a space after the initial dot.) 

```
. /venv/Scripts/activate
```

## Linux

```sh
$ git clone https://github.com/juhkure/IdleScape.git
Cloning into 'IdleScape'...
remote: Enumerating objects: 168, done.
remote: Counting objects: 100% (168/168), done.
remote: Compressing objects: 100% (109/109), done.
remote: Total 168 (delta 76), reused 129 (delta 48), pack-reused 0
Receiving objects: 100% (168/168), 25.39 KiB | 634.00 KiB/s, done.
Resolving deltas: 100% (76/76), done.
$ cd IdleScape/
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Automatic setup

In app.py on line 14 variable 'run_mode' allows you to choose if you wish to run according to .env variables or create and use a test database.
* 0 | Creates database connection according to .env variables and allows no configuration.
* 1 | Testing mode that creates a new database and a user for it. **Recommended for first run!** *
* 2 | Testing mode that uses the database and user created in run mode 1. Also allows resetting tables and populating the database from schema.sql and table filling with database/database_filler.py
* 3 | Quick testing mode. Skips all configuration in previous modes and assumes test database and user have already been created.

**CAUTION* Testing mode 1 requires your postgres password to create the testing database and a user for it. Do a manual setup instead if that worries you.

Then run flask from virtualenvironment (which we activated before):

```
(venv) $ flask run
```

## Manual setup

#### Option A: Create and name database according to variables found in code (steps shown with pictures)
* This allows you to run with all 1-3 testing/run modes (0 as well if you create .env) which if useful for testing.
* Can be done in command line or with pgAdmin 4

#### With pgAdmin 4: ####

![Create user](https://github.com/juhkure/IdleScape/blob/main/readme_images/create_user.png)
In pgAdmin4, create a user.

![Name user](https://github.com/juhkure/IdleScape/blob/main/readme_images/user_name.png)
Name the user 'idlescapetester' (same as in code)

![Password](https://github.com/juhkure/IdleScape/blob/main/readme_images/password.png)
In definition tab, add a password 'tsoha' (same as in code)

![Can login](https://github.com/juhkure/IdleScape/blob/main/readme_images/can_login.png)
In privileges tab, check 'Can login?' to ON
Then press Save

![Create database](https://github.com/juhkure/IdleScape/blob/main/readme_images/create_db.png)
Now let's create a database

![Name database](https://github.com/juhkure/IdleScape/blob/main/readme_images/db_name.png)
Name the database to 'idlescapetestdb' (same as in code)

![Set owner](https://github.com/juhkure/IdleScape/blob/main/readme_images/db_owner.png)
Set the owner to the user we just created (idlescapetester) and press Save

Now you should have the user and database created. Running the code in modes 1, 2, and 3 should work.

You can also create .env file in root directory with database url and secret key according to these variables if you wish to use mode 0 as well.

#### In terminal: ####

Connect to postgres and enter the following:

```
CREATE USER idlescapetester WITH PASSWORD 'tsoha' CREATEDB;
```

```
CREATE DATABASE idlescapetestdb WITH OWNER idlescapetester;
```

#### or option B: Create and name database freely

Steps are same as above but naming can be done freely. This requires you to setup a .env file with DATABASE_URL and SECRET_KEY according to your naming.
However you can only use run_mode 0 
