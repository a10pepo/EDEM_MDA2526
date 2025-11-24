select
    station_id,
    station_name,
    available_bikes,
    total_capacity,
    round(available_bikes::double / total_capacity * 100, 2) as occupancy_percent,
    time
from {{ ref('valenbisi') }}
