INSERT INTO activities (name) VALUES ('fishing');
INSERT INTO activities (name) VALUES ('parkour');
INSERT INTO activities (name) VALUES ('combat (accurate)');
INSERT INTO activities (name) VALUES ('combat (aggressive)');
INSERT INTO activities (name) VALUES ('combat (defensive)');
INSERT INTO activities (name) VALUES ('pray');
INSERT INTO activities (name) VALUES ('thieve');

InSERT INTO skills (name) VALUES ('attack');
INSERT INTO skills (name) VALUES ('hitpoints');
INSERT INTO skills (name) VALUES ('fishing');
INSERT INTO skills (name) VALUES ('agility');
INSERT INTO skills (name) VALUES ('prayer');
INSERT INTO skills (name) VALUES ('defence');
INSERT INTO skills (name) VALUES ('strength');
INSERT INTO skills (name) VALUES ('thieving');

INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (accurate)', 'attack', 75);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (accurate)', 'hitpoints', 25);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (aggressive)', 'strength', 75);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (aggressive)', 'hitpoints', 25);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (defensive)', 'defence', 75);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('combat (defensive)', 'hitpoints', 25);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('fishing', 'fishing', 100);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('parkour', 'agility', 100);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('pray', 'prayer', 100);
INSERT INTO activity_skill (activity_name, skill_name, base_xp) VALUES ('thieve', 'thieving', 100);
