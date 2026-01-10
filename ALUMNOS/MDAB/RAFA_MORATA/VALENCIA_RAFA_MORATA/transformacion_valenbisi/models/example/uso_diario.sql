{{ config(materialized='table') }}

SELECT
    station_id,
    station_name,
    DATE_TRUNC('day', timestamp) as fecha,
    AVG(available_bikes) as promedio_bicis,
    MIN(available_bikes) as minimo_bicis,
    MAX(available_bikes) as maximo_bicis
FROM
    public.valenbisi_raw
GROUP BY
    station_id,
    station_name,
    DATE_TRUNC('day', timestamp)