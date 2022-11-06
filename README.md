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
