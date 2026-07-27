SELECT
    station_id,
    station_name,
    DATE(timestamp) as fecha,
    ROUND(AVG(available_bikes), 2) as avg_bicis_dia,
    BOOL_OR(available_bikes = 0) as tuvo_falta_stock
FROM {{ source('raw_data', 'valenbisi_raw') }}
GROUP BY 1, 2, 3
ORDER BY fecha DESC, station_id ASC