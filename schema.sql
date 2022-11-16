CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE skills (
    name TEXT PRIMARY KEY
);

CREATE TABLE user_skills (
    user_id INTEGER REFERENCES users,
    skill_name TEXT REFERENCES skills,
    level INTEGER,
    experience INTEGER
);

CREATE TABLE activities (
    name TEXT PRIMARY KEY
);

CREATE TABLE user_activity (
    user_id INTEGER REFERENCES users,
    activity_name TEXT REFERENCES activities,
    action_at TIMESTAMP,
    active BOOLEAN
);

CREATE TABLE activity_skill (
    activity_name TEXT REFERENCES activities,
    skill_name TEXT REFERENCES skills,
    base_xp INTEGER
);