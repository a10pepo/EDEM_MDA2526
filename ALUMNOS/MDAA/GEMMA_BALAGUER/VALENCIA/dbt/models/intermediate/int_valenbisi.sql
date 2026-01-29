
SELECT
    number,
    address,
    lat,
    lon,
    available,
    free,
    total,
    ROUND((total - free)::numeric / total * 100, 2) AS occupancy_pct,
    open,
    updated_at,
    update_jcd
FROM {{ ref('stg_valenbisi') }}
