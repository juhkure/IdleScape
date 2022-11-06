CREATE TABLE users (
    name TEXT PRIMARY KEY,
    password TEXT
);

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE user_skills (
    name TEXT REFERENCES users,
    skill_id INTEGER REFERENCES skills,
    level INTEGER,
    experience INTEGER
);

CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE activity_skill (
    activity_id INTEGER REFERENCES activities,
    skill_id INTEGER REFERENCES skills,
    base_xp INTEGER
);