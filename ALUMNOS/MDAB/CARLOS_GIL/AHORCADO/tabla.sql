CREATE TABLE IF NOT EXISTS ahorcado2 (
        id SERIAL PRIMARY KEY,
        palabra VARCHAR(255) NOT NULL,
        letras_acertadas VARCHAR(100),
        letras_fallidas VARCHAR(100),
        intentos INTEGER NOT NULL,
        tiempo TIMESTAMP NOT NULL
);

SELECT * FROM ahorcado2;

INSERT INTO ahorcado2 (palabra, letras_acertadas, letras_fallidas, intentos, tiempo) VALUES
('MURCIELAGO', 'A', '', 1, '2021-01-01 12:00:00'),
('MURCIELAGO', 'A', 'B', 2, '2021-01-01 12:01:00'),
('MURCIELAGO', 'AC', 'B', 3, '2021-01-01 12:02:00'),
('MURCIELAGO', 'AC', 'BD', 4, '2021-01-01 12:04:00'),
('MURCIELAGO', 'ACE', 'BD', 5, '2021-01-01 12:05:00');
