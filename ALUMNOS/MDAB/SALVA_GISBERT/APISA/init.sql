CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    fechamuestreo TIMESTAMP NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    medicion DECIMAL NOT NULL
);

INSERT INTO sensor_data (code, fechamuestreo, unidad, medicion) VALUES
('sensor_01', '2026-01-13 10:00:00', 'Celsius', 35.5),
('sensor_01', '2026-01-13 10:05:00', 'Celsius', 36.2),
('sensor_02', '2026-01-13 10:10:00', 'Celsius', 40.0),
('sensor_03', '2026-01-13 10:15:00', 'Celsius', 22.1),
('sensor_01', '2026-01-13 10:20:00', 'Celsius', 37.8),
('sensor_02', '2026-01-13 10:25:00', 'Celsius', 39.5),
('sensor_04', '2026-01-13 10:30:00', 'Celsius', 45.0),
('sensor_05', '2026-01-13 10:35:00', 'Celsius', 33.3),
('sensor_03', '2026-01-13 10:40:00', 'Celsius', 24.5),
('sensor_01', '2026-01-13 10:45:00', 'Celsius', 38.1),
('sensor_02', '2026-01-13 10:50:00', 'Celsius', 41.2),
('sensor_06', '2026-01-13 10:55:00', 'Celsius', 30.0),
('sensor_04', '2026-01-13 11:00:00', 'Celsius', 44.8),
('sensor_05', '2026-01-13 11:05:00', 'Celsius', 34.1),
('sensor_01', '2026-01-13 11:10:00', 'Celsius', 39.0);