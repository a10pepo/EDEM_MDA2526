
  
    

  create  table "valenbisi_db"."public"."marts_ocupacion_por_hora__dbt_tmp"
  
  
    as
  
  (
    with base as (
    select i.*,
    s.hora_medicion
    from "valenbisi_db"."public"."int_ocupacion" i
    join "valenbisi_db"."public"."staging_valenbisi" s
    on i.numero_estacion = s.numero_estacion
    and i.momento_medicion = s.momento_medicion
),

horas as (
    select
        numero_estacion,
        nombre_estacion,
        capacidad_total,
        capacidad_real,
        extract(hour from momento_medicion) as hora,
        bicicletas_disponibles,
        huecos_disponibles,
        situacion_ocupacion
    from base
),

variaciones_hora as (
    select
        numero_estacion,
        extract(hour from momento_medicion) as hora,
        avg(variacion_bicis) as avg_variacion_bicis,
        avg(variacion_huecos) as avg_variacion_huecos
    from "valenbisi_db"."public"."int_evolucion_temporal"
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
        v.avg_variacion_bicis,
        v.avg_variacion_huecos
    from horas h
    left join variaciones_hora v
    on h.numero_estacion = v.numero_estacion
    and h.hora = v.hora
    group by h.numero_estacion, h.nombre_estacion, h.hora, v.avg_variacion_bicis, v.avg_variacion_huecos
)

select *
from metrics
order by numero_estacion, hora
  );
  