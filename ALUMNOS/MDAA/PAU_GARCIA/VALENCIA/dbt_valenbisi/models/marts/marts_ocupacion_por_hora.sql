with horas as (
    select
        numero_estacion,
        nombre_estacion,
        capacidad_total,
        capacidad_real,
        extract(hour from momento_medicion) as hora,
        bicicletas_disponibles,
        huecos_disponibles,
        situacion_ocupacion
    from {{ ref('int_ocupacion') }}
),


variaciones_hora as (
    select
        numero_estacion,
        extract(hour from momento_medicion) as hora,
        avg(variacion_bicis) as avg_variacion_bicis
    from {{ ref('int_evolucion_temporal') }}
    group by numero_estacion, extract(hour from momento_medicion)
),

metrics as (
    select
        h.numero_estacion,
        h.nombre_estacion,
        h.hora,
        count(*) as total_mediciones,
        max(h.capacidad_real) as capacidad_real,
        avg(h.bicicletas_disponibles) as avg_bicis,
        avg(h.huecos_disponibles) as avg_huecos,
        avg(case when situacion_ocupacion = 'vacía' then 1.0 else 0 end) as pct_vacia,
        avg(case when situacion_ocupacion = 'llena' then 1.0 else 0 end) as pct_llena,
        v.avg_variacion_bicis
    from horas h
    left join variaciones_hora v
    on h.numero_estacion = v.numero_estacion
    and h.hora = v.hora
    group by h.numero_estacion, h.nombre_estacion, h.hora, v.avg_variacion_bicis
)

select *
from metrics
order by numero_estacion, hora
