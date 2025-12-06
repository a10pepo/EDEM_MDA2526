

SELECT
    number,
    address,
    updated_at::date AS date,
    AVG(available) AS avg_available,
    AVG(free) AS avg_free,
    AVG(total) AS avg_total,
    ROUND(AVG((total - free)::numeric / total * 100), 2) AS avg_occupancy_pct
FROM "pruebadb"."public"."stg_valenbisi"
GROUP BY number, address, updated_at::date
ORDER BY number, date