CREATE TABLE players
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    charactername VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL,
    dt INTEGER NOT NULL,
    sp INTEGER NOT NULL,
    ryo INTEGER NOT NULL
);

CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL,
    affected_field VARCHAR(255) NOT NULL,
    old_value VARCHAR(255) NOT NULL,
    new_value VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    date DATE NOT NULL
);