
  
  create view "dev"."main"."availability__dbt_tmp" as (
    select
    station_id,
    station_name,
    available_bikes,
    available_bike_stands,
    total_capacity,
    state_station,
    time
from "dev"."main"."valenbisi"
  );
