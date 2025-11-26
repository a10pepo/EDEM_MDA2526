with base as (
    select *
    from {{ ref('int_ocupacion') }}
),

medias as (
    select
        numero_estacion,
        nombre_estacion,
        capacidad_total,
        avg(case when situacion_ocupacion in ('vacía') then 1.0 else 0 end) as pct_vacia,
        avg(case when situacion_ocupacion in ('casi vacía') then 1.0 else 0 end) as pct_casi_vacia,
        --Se ponderan las situaciones, no es lo mismo estar 'vacía' que 'casi vacía'
        --Esta ponderacion no se muestra al cliente pero es útil para ordenar
        --Hará que cuando haya estaciones con el mismo pct_vacia, se muestren primero las que tengas más pct de casi vacía
        --Se utiliza 0,1 porque se valora que estar vacía es mucho peor, pero depende del cliente como lo valore
        avg(
            case 
                when situacion_ocupacion = 'vacía' then 1.0
                when situacion_ocupacion = 'casi vacía' then 0.1
                else 0
            end
        ) as ponderacion
    from base
    group by numero_estacion, nombre_estacion, capacidad_total
)

select numero_estacion, nombre_estacion, capacidad_total, pct_vacia, pct_casi_vacia
from medias
order by ponderacion desc
