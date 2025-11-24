select
    station_id,
    station_name,
    available_bikes,
    available_bike_stands,
    total_capacity,
    state_station,
    time
from {{ ref('valenbisi') }}

