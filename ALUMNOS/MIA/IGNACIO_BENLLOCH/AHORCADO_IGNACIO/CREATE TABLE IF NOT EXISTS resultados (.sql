CREATE TABLE IF NOT EXISTS resultados (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        palabra VARCHAR(100) NOT NULL,
        letras_acertadas VARCHAR(255),
        letras_falladas VARCHAR(255),
        intentos INT,
        tiempo TIMESTAMPTZ DEFAULt now()
    );

select * from resultados