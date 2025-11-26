
  
    

  create  table "valenbisi_db"."public"."marts_horas_pico_por_estacion__dbt_tmp"
  
  
    as
  
  (
    with variaciones_hora as (
    select
        numero_estacion,
        extract(hour from momento_medicion) as hora,
        avg(variacion_bicis) as avg_variacion_bicis
    from "valenbisi_db"."public"."int_evolucion_temporal"
    group by numero_estacion, extract(hour from momento_medicion)
),

bicis_hora as (
    select
        numero_estacion,
        extract(hour from momento_medicion) as hora,
        avg(bicicletas_disponibles) as avg_bicis
    from "valenbisi_db"."public"."int_ocupacion"
    group by numero_estacion, extract(hour from momento_medicion)
),

huecos_hora as (
    select
        numero_estacion,
        extract(hour from momento_medicion) as hora,
        avg(huecos_disponibles) as avg_huecos
    from "valenbisi_db"."public"."int_ocupacion"
    group by numero_estacion, extract(hour from momento_medicion)
),

-- Hora(s) de mayor variación (llenado/vaciado rápido)
pico_variacion as (
    select
        numero_estacion,
        string_agg(cast(hora as text), ', ') as hora_max_variacion
    from variaciones_hora v
    where avg_variacion_bicis = (
        select max(avg_variacion_bicis)
        from variaciones_hora
        where numero_estacion = v.numero_estacion
    )
    group by numero_estacion
),

-- Hora(s) con más bicis disponibles
pico_bicis as (
    select
        numero_estacion,
        string_agg(cast(hora as text), ', ') as hora_max_bicis
    from bicis_hora b
    where avg_bicis = (
        select max(avg_bicis)
        from bicis_hora
        where numero_estacion = b.numero_estacion
    )
    group by numero_estacion
),

-- Hora(s) con más huecos disponibles
pico_huecos as (
    select
        numero_estacion,
        string_agg(cast(hora as text), ', ') as hora_max_huecos
    from huecos_hora h
    where avg_huecos = (
        select max(avg_huecos)
        from huecos_hora
        where numero_estacion = h.numero_estacion
    )
    group by numero_estacion
),

total as (
    select
        numero_estacion,
        nombre_estacion,
        avg(bicicletas_disponibles) as avg_bicis,
        avg(huecos_disponibles) as avg_huecos,
        avg(case when situacion_ocupacion in ('vacía','casi vacía') then 1.0 else 0 end) as pct_vacia,
        avg(case when situacion_ocupacion in ('llena','casi llena') then 1.0 else 0 end) as pct_llena
    from "valenbisi_db"."public"."int_ocupacion"
    group by numero_estacion, nombre_estacion
)

select
    t.numero_estacion,
    t.nombre_estacion,
    t.avg_bicis,
    t.avg_huecos,
    t.pct_vacia,
    t.pct_llena,
    pv.hora_max_variacion,
    pb.hora_max_bicis,
    ph.hora_max_huecos
from total t
left join pico_variacion pv on t.numero_estacion = pv.numero_estacion
left join pico_bicis pb on t.numero_estacion = pb.numero_estacion
left join pico_huecos ph on t.numero_estacion = ph.numero_estacion
order by t.numero_estacion
  );
  