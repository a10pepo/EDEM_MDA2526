
  create view "pruebadb"."public"."mart_valenbisi__dbt_tmp"
    
    
  as (
    -- models/marts/mart_valenbisi.sql

with base as (
    select
        address,
        available,
        total,
        available::decimal / nullif(total,0) as availability_ratio
    from "pruebadb"."public"."int_valenbisi"
)

select
    address,
    available,
    total,
    availability_ratio
from base
order by availability_ratio desc
  );