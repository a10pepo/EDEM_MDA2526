
  
  create view "dev"."main"."hourly_summary__dbt_tmp" as (
    select
    date_trunc('hour', time) as hour,
    sum(available_bikes) as total_bikes,
    sum(available_bike_stands) as total_free_stands
from "dev"."main"."valenbisi"
group by hour
order by hour
  );
