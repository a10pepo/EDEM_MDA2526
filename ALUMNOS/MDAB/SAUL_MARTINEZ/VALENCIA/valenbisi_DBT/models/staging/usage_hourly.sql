SELECT
    station_id,
    station_name,
    DATE_TRUNC('hour', timestamp) as hora,
    ROUND(AVG(available_bikes), 2) as avg_bicis,
    MAX(available_bikes) as max_bicis,
    MIN(available_bikes) as min_bicis,
    COUNT(*) as num_registros
FROM {{ source('raw_data', 'valenbisi_raw') }}
GROUP BY 1, 2, 3
ORDER BY hora DESC, station_id ASC