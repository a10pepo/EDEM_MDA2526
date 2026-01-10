{{ config(materialized='table') }}

SELECT
    station_id,
    station_name,
    DATE_TRUNC('hour', timestamp) as hora,
    AVG(available_bikes) as promedio_bicis_disponibles,
    AVG(available_slots) as promedio_espacios_libres,
    MAX(total_capacity) as capacidad_total
FROM
    public.valenbisi_raw
GROUP BY
    station_id,
    station_name,
    DATE_TRUNC('hour', timestamp)