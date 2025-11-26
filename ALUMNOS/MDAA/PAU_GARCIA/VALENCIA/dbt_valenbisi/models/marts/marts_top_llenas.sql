with base as (
    select *
    from {{ ref('int_ocupacion') }}
),

medias as (
    select
        numero_estacion,
        nombre_estacion,
        capacidad_total,
        avg(case when situacion_ocupacion in ('llena') then 1.0 else 0 end) as pct_llena,
        avg(case when situacion_ocupacion in ('casi llena') then 1.0 else 0 end) as pct_casi_llena,
        --Se ponderan las situaciones, no es lo mismo estar 'llena' que 'casi llena'
        --Esta ponderacion no se muestra al cliente pero es útil para ordenar
        --Hará que cuando haya estaciones con el mismo pct_llena, se muestren primero las que tengas más pct de casi llena
        --Se utiliza 0,1 porque se valora que estar llena es mucho peor, pero depende del cliente como lo valore
        avg(
            case 
                when situacion_ocupacion = 'llena' then 1.0
                when situacion_ocupacion = 'casi llena' then 0.1
                else 0
            end
        ) as ponderacion
    from base
    group by numero_estacion, nombre_estacion, capacidad_total
)

select numero_estacion, nombre_estacion, capacidad_total, pct_llena, pct_casi_llena
from medias
order by ponderacion desc
