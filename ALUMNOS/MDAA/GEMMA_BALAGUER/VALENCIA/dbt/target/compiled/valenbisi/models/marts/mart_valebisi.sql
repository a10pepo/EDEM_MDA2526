

SELECT
    number,
    address,
    lat,
    lon,
    SUM(available) AS total_available,
    SUM(free) AS total_free,
    SUM(total) AS total_capacity,
    ROUND(AVG(occupancy_pct), 2) AS avg_occupancy_pct,
    MAX(updated_at) AS last_update,
    MAX(update_jcd) AS last_update_jcd
FROM "pruebadb"."public"."int_valenbisi"
GROUP BY number, address, lat, lon