CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE user_skills (
    user_id INTEGER REFERENCES users,
    skill_id INTEGER REFERENCES skills,
    level INTEGER,
    experience INTEGER
);

CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE user_activity (
    user_id INTEGER REFERENCES users,
    activity_id INTEGER REFERENCES activities,
    action_at TIMESTAMP,
    active BOOLEAN
);

CREATE TABLE activity_skill (
    activity_id INTEGER REFERENCES activities,
    skill_id INTEGER REFERENCES skills,
    base_xp INTEGER
);