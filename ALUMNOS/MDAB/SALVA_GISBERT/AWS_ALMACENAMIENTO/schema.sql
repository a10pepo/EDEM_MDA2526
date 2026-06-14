DROP TABLE IF EXISTS callups;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age BETWEEN 15 AND 45),
    position TEXT NOT NULL CHECK (
        position IN ('goalkeeper', 'defender', 'midfielder', 'forward')
    ),
    status TEXT NOT NULL DEFAULT 'available' CHECK (
        status IN ('available', 'injured', 'suspended')
    ),
    last_medical_review DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE matches (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    opponent TEXT NOT NULL,
    match_date DATE NOT NULL,
    stadium TEXT NOT NULL,
    max_callups INTEGER NOT NULL CHECK (max_callups BETWEEN 11 AND 26),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE callups (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    match_id BIGINT NOT NULL,
    player_id BIGINT NOT NULL,
    callup_status TEXT NOT NULL CHECK (
        callup_status IN ('called', 'confirmed', 'absent', 'injured')
    ),
    shirt_number INTEGER NOT NULL CHECK (shirt_number BETWEEN 1 AND 99),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches (id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players (id) ON DELETE CASCADE,
    UNIQUE (match_id, player_id),
    UNIQUE (match_id, shirt_number)
);

CREATE INDEX idx_players_status ON players (status);
CREATE INDEX idx_matches_match_date ON matches (match_date);
CREATE INDEX idx_callups_match_id ON callups (match_id);
