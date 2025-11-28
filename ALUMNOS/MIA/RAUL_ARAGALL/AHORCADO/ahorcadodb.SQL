CREATE TABLE IF NOT EXISTS ahorcado(
    id        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    palabra VARCHAR,
    letras_acertadas VARCHAR,
    letras_fallads VARCHAR,
    intentos INTEGER,
    tiempo TIMESTAMPTZ NOT NULL DEFAULT now()
)
TRUNCATE ahorcado;
-- -- DROP TABLE ahorcado

SELECT * FROM ahorcado