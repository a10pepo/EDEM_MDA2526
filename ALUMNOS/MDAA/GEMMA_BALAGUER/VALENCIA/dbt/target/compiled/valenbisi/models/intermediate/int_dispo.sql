SELECT
    number,
    address,
    lat,
    lon,
    open,
    total,
    free,
    available,
    CASE
        WHEN open IS FALSE THEN 'CERRADA'
        WHEN available = 0 THEN 'VACÍA'
        WHEN free = 0 THEN 'LLENA'
        ELSE 'DISPONIBLE'
    END AS status,
    updated_at
FROM "pruebadb"."public"."stg_valenbisi"