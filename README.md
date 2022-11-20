# IdleScape

A [RuneScape](https://www.runescape.com/) influenced idle/[incremental](https://en.wikipedia.org/wiki/Incremental_game) -game which's objective is very simple: level and build up your character slowly but surely with mostly inactive gameplay.

Idlescape's goal isn't to provide a highly interactive gameplay loop but rather a casual experience that allows you to attend to life's boring but obligatory tasks like work and school, all the while you're gaining progression in a game!

The game's initial page allows the user to create and log in to their character/account. Upon logging in, the main page will show them:

- Skills and their levels
- Total level and experience
- User's current chosen activity
- Experience amount that the activity produces

The player can choose an activity to log their participation in from a list of different activities. This chosen activity determines the amount of experience and the target skill this experience goes to. For example, a combat activity would reward the player with experience towards combat skills like strength and hitpoints. Or the player could choose a skilling activity like fishing to further their levels in the fishing skill.

Player's skills are considered their "stats", and each of these stats/skills start from level 1 and can be levelled up all the way to 99. Each new level will require more experience than the previous one.

## Plans

The current plan is to do calculations and database logic within the backend server. Frontend will be done with JavaScript to allow a more visual and smoother user experience. At it's core, the game's database consists of just 6 tables to track users, their skills, and their chosen activity.

Further plans consist of things like unlocks/achievements and items that allows the player to further plan and customize their progression but their implementation is for now, out of reach.

# Instructions for testing

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

### Automatic setup ###

In app.py on line 14 variable 'run_mode' allows you to choose if you wish to run according to .env variables or create and use a test database.
* 0 | Creates database connection according to .env variables and allows no configuration.
* 1 | Testing mode that creates a new database and a user for it. **Recommended for first run!** *
* 2 | Testing mode that uses the database and user created in run mode 1. Also allows resetting tables and populating the database from schema.sql and table filling with database/database_filler.py
* 3 | Quick testing mode. Skips all configuration in previous modes and assumes test database and user have already been created.

**CAUTION* Testing mode 1 requires your postgres password to create the testing database and a user for it. Do a manual setup instead if that worries you.

### Manual setup ###

#### A: Create and name database according to variables found in code ####
* This allows you to run with all 1-3 testing modes (0 as well if you create .env) which if useful for testing.
* Can be done in command line or with pgAdmin 4


#### or B: Create and name database freely ####

winpty python -m venv venv
. venv/Scripts/activate
