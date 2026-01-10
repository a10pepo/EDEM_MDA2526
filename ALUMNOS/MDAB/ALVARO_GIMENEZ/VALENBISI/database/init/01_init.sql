CREATE TABLE IF NOT EXISTS valenbisi_history (
    id SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL,
    station_name TEXT,
    available_bikes INTEGER,
    available_slots INTEGER,
    station_status CHAR(1),
    total_capacity INTEGER,
    timestamp TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_valenbisi_station_time
ON valenbisi_history (station_id, timestamp);
