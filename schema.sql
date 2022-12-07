CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS skills (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS user_skills (
    user_id INTEGER REFERENCES users,
    skill_name TEXT REFERENCES skills,
    level INTEGER,
    experience INTEGER,
    experience_left INTEGER
);

CREATE TABLE IF NOT EXISTS activities (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS user_activity (
    user_id INTEGER REFERENCES users,
    activity_name TEXT REFERENCES activities,
    action_at TIMESTAMP,
    active BOOLEAN
);

CREATE TABLE IF NOT EXISTS activity_skill (
    activity_name TEXT REFERENCES activities,
    skill_name TEXT REFERENCES skills,
    base_xp INTEGER
);
