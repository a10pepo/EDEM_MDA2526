CREATE TABLE valenbisi_raw (
    id SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL,
    station_name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    available_bikes INTEGER,
    available_slots INTEGER,
    station_status VARCHAR(50),
    total_capacity INTEGER,
    timestamp TIMESTAMP NOT NULL
);