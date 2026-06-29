-- ========================================================================
-- Modelo de datos transaccional (OLTP) en PostgreSQL / RDS
-- Normalizado en 3FN. La relación vuelo<->pasajero es N:M con atributo
-- de estado, por lo que se modela con la tabla puente flight_passengers.
-- ========================================================================

CREATE TABLE IF NOT EXISTS airplanes (
    plate_number          VARCHAR(20)  PRIMARY KEY,
    type                  VARCHAR(100) NOT NULL,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    capacity              INTEGER      NOT NULL CHECK (capacity > 0),
    owner_id              VARCHAR(20),
    owner_name            VARCHAR(150),
    hangar_id             VARCHAR(20),
    fuel_capacity         INTEGER
);

CREATE TABLE IF NOT EXISTS passengers (
    passenger_id  VARCHAR(20)  PRIMARY KEY,
    name          VARCHAR(150) NOT NULL,
    national_id   VARCHAR(20)  NOT NULL UNIQUE,
    date_of_birth DATE
);

CREATE TABLE IF NOT EXISTS flights (
    flight_id        VARCHAR(30) PRIMARY KEY,
    plate_number     VARCHAR(20) NOT NULL REFERENCES airplanes (plate_number),
    arrival_time     TIMESTAMP,
    departure_time   TIMESTAMP,
    fuel_consumption INTEGER,
    occupied_seats   INTEGER,
    origin           VARCHAR(100),
    destination      VARCHAR(100)
);

-- Tabla puente de la relación N:M con el estado del pasajero en el vuelo
CREATE TABLE IF NOT EXISTS flight_passengers (
    flight_id    VARCHAR(30) NOT NULL REFERENCES flights (flight_id),
    passenger_id VARCHAR(20) NOT NULL REFERENCES passengers (passenger_id),
    status       VARCHAR(20) NOT NULL,
    PRIMARY KEY (flight_id, passenger_id)
);

CREATE INDEX IF NOT EXISTS idx_flights_plate ON flights (plate_number);
CREATE INDEX IF NOT EXISTS idx_fp_passenger ON flight_passengers (passenger_id);
