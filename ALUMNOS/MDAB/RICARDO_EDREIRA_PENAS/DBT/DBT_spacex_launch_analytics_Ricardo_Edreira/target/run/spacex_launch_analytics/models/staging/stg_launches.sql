
  
  create view "dev"."main"."stg_launches__dbt_tmp" as (
    -- stg_launches.sql
-- Modelo de staging para lanzamientos de SpaceX
-- Autor: Ricardo Edreira



with source as (
    select * from "dev"."main"."raw_launches"
),

cleaned as (
    select
        id as launch_id,
        name as mission_name,
        flight_number,
        
        -- Parsear fecha
        try_cast(date_utc as timestamp) as launch_date,
        extract(year from try_cast(date_utc as timestamp)) as launch_year,
        extract(month from try_cast(date_utc as timestamp)) as launch_month,
        
        -- Campo success ya viene como boolean
        success as is_success,
        
        -- Clasificar resultado
        case 
            when success = true then 'Exitoso'
            when success = false then 'Fallido'
            else 'Pendiente'
        end as launch_status,
        
        rocket_id,
        launchpad_id,
        
        -- Limpiar detalles
        nullif(trim(details), '') as mission_details,
        
        -- Flag para lanzamientos futuros
        coalesce(upcoming, false) as is_upcoming
        
    from source
)

select * from cleaned
  );
