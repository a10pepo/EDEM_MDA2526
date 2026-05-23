-- stg_rockets.sql
-- Modelo de staging para cohetes de SpaceX
-- Autor: Ricardo Edreira



with source as (
    select * from "dev"."main"."raw_rockets"
),

cleaned as (
    select
        id as rocket_id,
        name as rocket_name,
        type as rocket_type,
        
        -- Campo active ya viene como boolean
        coalesce(active, false) as is_active,
        
        try_cast(stages as integer) as num_stages,
        try_cast(boosters as integer) as num_boosters,
        try_cast(cost_per_launch as decimal(18,2)) as cost_per_launch_usd,
        try_cast(success_rate_pct as decimal(5,2)) as success_rate_pct,
        try_cast(first_flight as date) as first_flight_date,
        
        country,
        company,
        
        try_cast(height_meters as decimal(10,2)) as height_meters,
        try_cast(diameter_meters as decimal(10,2)) as diameter_meters,
        try_cast(mass_kg as integer) as mass_kg,
        
        nullif(trim(description), '') as description
        
    from source
)

select * from cleaned