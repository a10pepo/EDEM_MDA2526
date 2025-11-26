with last_update as (
    select *
    from {{ ref('int_last_update') }}
),

ocupacion as (
    select *
    from {{ ref('int_ocupacion') }}
),

estado_actual as (
    select distinct on (l.numero_estacion)
        l.numero_estacion,
        l.nombre_estacion,
        l.latitud,
        l.longitud,
        o.bicicletas_disponibles,
        o.huecos_disponibles,
        o.capacidad_total,
        o.capacidad_real,
        o.no_disponibles,
        o.situacion_ocupacion,
        l.momento_medicion
    from last_update l
    join ocupacion o
    on l.numero_estacion = o.numero_estacion
    and l.momento_medicion = o.momento_medicion
)

select *
from estado_actual
order by numero_estacion
