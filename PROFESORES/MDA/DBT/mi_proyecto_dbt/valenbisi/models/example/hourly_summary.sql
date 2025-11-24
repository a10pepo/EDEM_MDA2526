select
    date_trunc('hour', time) as hour,
    sum(available_bikes) as total_bikes,
    sum(available_bike_stands) as total_free_stands
from {{ ref('valenbisi') }}
group by hour
order by hour

