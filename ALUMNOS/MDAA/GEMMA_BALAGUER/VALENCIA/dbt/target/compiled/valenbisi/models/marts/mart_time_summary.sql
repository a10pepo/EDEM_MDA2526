SELECT date, SUM(avg_available) AS total_available, 
SUM(avg_free) AS total_free, 
SUM(avg_total) AS total_capacity, 
ROUND(AVG(avg_occupancy_pct), 2) AS avg_occupancy_pct FROM "pruebadb"."public"."int_valenbisi_time" 
GROUP BY date 
ORDER BY date