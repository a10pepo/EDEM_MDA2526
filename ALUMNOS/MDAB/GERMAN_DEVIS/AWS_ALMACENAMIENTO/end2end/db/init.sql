-- F1 schema — run once against RDS before executing load_rds.py
-- psql -h $PGHOST -U $PGUSER -d $PGDATABASE -f db/init.sql

CREATE TABLE IF NOT EXISTS teams (
    team_id        VARCHAR(10)  PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    base           VARCHAR(100),
    team_principal VARCHAR(100),
    power_unit     VARCHAR(50),
    founded_year   SMALLINT,
    championships  SMALLINT     DEFAULT 0
);

CREATE TABLE IF NOT EXISTS drivers (
    driver_id        VARCHAR(10)  PRIMARY KEY,
    team_id          VARCHAR(10)  NOT NULL REFERENCES teams(team_id),
    code             CHAR(3)      NOT NULL UNIQUE,
    name             VARCHAR(100) NOT NULL,
    nationality      VARCHAR(50),
    date_of_birth    DATE,
    permanent_number SMALLINT
);

CREATE TABLE IF NOT EXISTS races (
    race_id  VARCHAR(15)  PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    circuit  VARCHAR(100),
    country  VARCHAR(50),
    date     DATE         NOT NULL,
    season   SMALLINT     NOT NULL,
    round    SMALLINT     NOT NULL,
    laps     SMALLINT
);

CREATE TABLE IF NOT EXISTS results (
    race_id        VARCHAR(15)  NOT NULL REFERENCES races(race_id),
    driver_id      VARCHAR(10)  NOT NULL REFERENCES drivers(driver_id),
    grid_position  SMALLINT     NOT NULL DEFAULT 0,
    final_position SMALLINT     NOT NULL DEFAULT 0,
    points         NUMERIC(5,2) NOT NULL DEFAULT 0,
    status         VARCHAR(20)  NOT NULL,
    PRIMARY KEY (race_id, driver_id)
);
