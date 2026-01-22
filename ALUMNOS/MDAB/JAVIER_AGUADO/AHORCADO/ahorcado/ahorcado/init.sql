CREATE TABLE IF NOT EXISTS intento_ahorcado (
    id SERIAL PRIMARY KEY,
    palabra TEXT,
    letras_acertadas TEXT,
    letras_falladas TEXT,
    intentos INTEGER,
    tiempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

