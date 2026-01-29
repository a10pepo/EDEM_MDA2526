CREATE TABLE IF NOT EXISTS resultados (
    id SERIAL PRIMARY KEY,
    palabra VARCHAR(255),
    letras_acertadas VARCHAR(255),
    letras_falladas VARCHAR(255),
    intentos INT,
    tiempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
