-- ========================================================================
-- Modelo analítico (OLAP) en Amazon Redshift
-- EL: se replica la estructura transaccional (sin transformaciones).
-- Redshift no fuerza PK/FK (son informativas para el optimizador).
-- Se usan DISTSTYLE/SORTKEY para un buen rendimiento de consulta.
-- ========================================================================

CREATE TABLE IF NOT EXISTS airplanes (
    plate_number          VARCHAR(20)  NOT NULL,
    type                  VARCHAR(100) NOT NULL,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    capacity              INTEGER      NOT NULL,
    owner_id              VARCHAR(20),
    owner_name            VARCHAR(150),
    hangar_id             VARCHAR(20),
    fuel_capacity         INTEGER,
    PRIMARY KEY (plate_number)
)
DISTSTYLE ALL
SORTKEY (plate_number);

CREATE TABLE IF NOT EXISTS passengers (
    passenger_id  VARCHAR(20)  NOT NULL,
    name          VARCHAR(150) NOT NULL,
    national_id   VARCHAR(20)  NOT NULL,
    date_of_birth DATE,
    PRIMARY KEY (passenger_id)
)
DISTSTYLE ALL
SORTKEY (passenger_id);

CREATE TABLE IF NOT EXISTS flights (
    flight_id        VARCHAR(30) NOT NULL,
    plate_number     VARCHAR(20) NOT NULL,
    arrival_time     TIMESTAMP,
    departure_time   TIMESTAMP,
    fuel_consumption INTEGER,
    occupied_seats   INTEGER,
    origin           VARCHAR(100),
    destination      VARCHAR(100),
    PRIMARY KEY (flight_id)
)
DISTKEY (plate_number)
SORTKEY (departure_time);

CREATE TABLE IF NOT EXISTS flight_passengers (
    flight_id    VARCHAR(30) NOT NULL,
    passenger_id VARCHAR(20) NOT NULL,
    status       VARCHAR(20) NOT NULL,
    PRIMARY KEY (flight_id, passenger_id)
)
DISTKEY (flight_id)
SORTKEY (flight_id);
