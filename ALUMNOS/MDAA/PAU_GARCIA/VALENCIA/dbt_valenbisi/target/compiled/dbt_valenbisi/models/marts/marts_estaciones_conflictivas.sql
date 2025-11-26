with base as (

    select *
    from "valenbisi_db"."public"."int_ocupacion"

),

medias as (

    select
        numero_estacion,
        nombre_estacion,
        capacidad_total,

        -- Porcentaje de tiempo cada estación estuvo vacía o casi vacía
        avg(case when situacion_ocupacion in ('vacía','casi vacía') then 1.0 else 0 end) as pct_vacia,

        -- Porcentaje de tiempo cada estación estuvo llena o casi llena
        avg(case when situacion_ocupacion in ('llena','casi llena') then 1.0 else 0 end) as pct_llena,

        -- Porcentaje de tiempo fuera de servicio
        avg(case when estado_estacion != 'Disponible' then 1.0 else 0 end) as pct_tiempo_fuera_servicio,

        -- Variabilidad en bicicletas disponibles
        stddev(bicicletas_disponibles) as std_bicis_disponibles,

        -- Variabilidad en huecos disponibles
        stddev(huecos_disponibles) as std_huecos_disponibles

    from base
    group by numero_estacion, nombre_estacion, capacidad_total

),

ranked as (

    -- Rankear top 10 más llenas y top 10 más vacías
    select *,
        row_number() over (order by pct_llena desc) as rank_llena,
        row_number() over (order by pct_vacia desc) as rank_vacia
    from medias

)

-- Seleccionamos las top 10 más llenas y top 10 más vacías
select *
from ranked
where rank_llena <= 10
or rank_vacia <= 10
order by rank_llena, rank_vacia