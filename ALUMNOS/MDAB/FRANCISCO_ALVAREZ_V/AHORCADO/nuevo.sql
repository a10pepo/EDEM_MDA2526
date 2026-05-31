CREATE TABLE IF NOT EXISTS public.intentos_ahorcado (
    id               BIGSERIAL PRIMARY KEY,
    palabra          TEXT        NOT NULL,                       -- palabra a adivinar
    letras_acertadas TEXT        NOT NULL DEFAULT '',            -- letras usadas que acertaron (string o CSV)
    letras_falladas  TEXT        NOT NULL DEFAULT '',            -- letras falladas (string o CSV)
    intentos         INTEGER     NOT NULL CHECK (intentos >= 0), -- nº de intentos empleados
    tiempo           TIMESTAMPTZ NOT NULL DEFAULT NOW()          -- momento del registro
);

INSERT INTO public.intentos_ahorcado (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
VALUES
    ('MURCIELAGO', 'A',   '',   1, '2021-01-01 12:00:00'),
    ('MURCIELAGO', 'A',   'B',  2, '2021-01-01 12:01:00'),
    ('MURCIELAGO', 'AC',  'B',  3, '2021-01-01 12:02:00'),
    ('MURCIELAGO', 'AC',  'BD', 4, '2021-01-01 12:04:00'),
    ('MURCIELAGO', 'ACE', 'BD', 5, '2021-01-01 12:05:00');


CREATE INDEX IF NOT EXISTS idx_intentos_palabra ON public.intentos_ahorcado (palabra);
CREATE INDEX IF NOT EXISTS idx_intentos_tiempo  ON public.intentos_ahorcado (tiempo DESC);

SELECT * FROM public.intentos_ahorcado;

