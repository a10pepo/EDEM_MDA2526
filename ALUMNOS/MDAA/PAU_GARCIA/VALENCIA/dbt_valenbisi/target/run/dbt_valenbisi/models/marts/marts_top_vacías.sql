
  
    

  create  table "valenbisi_db"."public"."marts_top_vacías__dbt_tmp"
  
  
    as
  
  (
    with base as (
    select *
    from "valenbisi_db"."public"."int_ocupacion"
),

medias as (
    select
        numero_estacion,
        nombre_estacion,
        capacidad_total,
        avg(case when situacion_ocupacion in ('vacía','casi vacía') then 1.0 else 0 end) as pct_vacia,
        --Se ponderan las situaciones, no es lo mismo estar 'vacía' que 'casi vacía'
        --Se utiliza esta ponderación para el ranking de más problemáticas
        avg(
            case 
                when situacion_ocupacion = 'vacía' then 1.0
                when situacion_ocupacion = 'casi vacía' then 0.5
                else 0
            end
        ) as ponderacion
    from base
    group by numero_estacion, nombre_estacion, capacidad_total
)

select *
from medias
order by ponderacion desc
limit 10
  );
  