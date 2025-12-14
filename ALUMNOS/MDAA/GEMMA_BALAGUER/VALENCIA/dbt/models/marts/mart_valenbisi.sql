-- models/marts/mart_valenbisi.sql
{{ config(
    materialized='table'
) }}

with base as (
    select
        address,
        available,
        total,
        available::decimal / nullif(total,0) as availability_ratio
    from {{ ref('int_valenbisi') }}
)

select
    address,
    available,
    total,
    availability_ratio
from base
order by availability_ratio desc
