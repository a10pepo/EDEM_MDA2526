SELECT 'CREATE DATABASE ahorcado_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ahorcado_db')\gexec

\c ahorcado_db;

CREATE TABLE IF NOT EXISTS juego_palabras (
    palabra VARCHAR(30) NOT NULL,
    letras_acertadas TEXT,
    letras_falladas TEXT,
    intentos INTEGER DEFAULT 0,
    tiempo TIMESTAMP
);