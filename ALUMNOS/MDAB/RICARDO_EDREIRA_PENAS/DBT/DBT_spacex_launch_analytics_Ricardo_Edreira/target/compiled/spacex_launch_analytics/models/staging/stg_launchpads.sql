-- stg_launchpads.sql
-- Modelo de staging para plataformas de lanzamiento
-- Autor: Ricardo Edreira



with source as (
    select * from "dev"."main"."raw_launchpads"
),

cleaned as (
    select
        id as launchpad_id,
        name as launchpad_name,
        full_name as launchpad_full_name,
        locality,
        region,
        
        try_cast(latitude as decimal(10,6)) as latitude,
        try_cast(longitude as decimal(10,6)) as longitude,
        
        try_cast(launch_attempts as integer) as total_launch_attempts,
        try_cast(launch_successes as integer) as total_launch_successes,
        
        -- Calcular tasa de éxito de la plataforma
        case 
            when try_cast(launch_attempts as integer) > 0 
            then round(try_cast(launch_successes as decimal) / try_cast(launch_attempts as decimal) * 100, 2)
            else 0
        end as success_rate_pct,
        
        status as launchpad_status,
        nullif(trim(details), '') as description
        
    from source
)

select * from cleaned