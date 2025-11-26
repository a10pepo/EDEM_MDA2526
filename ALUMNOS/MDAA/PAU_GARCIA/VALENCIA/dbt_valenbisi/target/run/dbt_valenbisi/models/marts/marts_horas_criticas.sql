
  
    

  create  table "valenbisi_db"."public"."marts_horas_criticas__dbt_tmp"
  
  
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

-- Convertimos la hora a entero para agrupar por hora del día (0-23)
horas as (
    select
        numero_estacion,
        nombre_estacion,
        capacidad_total,
        extract(hour from hora_medicion) as hora,
        bicicletas_disponibles,
        huecos_disponibles,
        situacion_ocupacion
    from base
),

metrics as (
    select
        numero_estacion,
        nombre_estacion,
        hora,
        count(*) as total_mediciones,

        -- Promedio de bicicletas disponibles por hora
        avg(bicicletas_disponibles) as avg_bicis,

        -- Promedio de huecos disponibles por hora
        avg(huecos_disponibles) as avg_huecos,

        -- Promedio de ocupación por hora
        avg(capacidad_total - huecos_disponibles) as avg_ocupacion,

        -- Variabilidad para ver rotación de bicis por hora
        stddev(bicicletas_disponibles) as std_bicis,
        stddev(huecos_disponibles) as std_huecos,

        -- Porcentaje de veces que la estación estuvo vacía o casi vacía
        avg(case when situacion_ocupacion in ('vacía','casi vacía') then 1.0 else 0 end) as pct_vacia,

        -- Porcentaje de veces que la estación estuvo llena o casi llena
        avg(case when situacion_ocupacion in ('llena','casi llena') then 1.0 else 0 end) as pct_llena

    from horas
    group by numero_estacion, nombre_estacion, hora, capacidad_total
)

select *
from metrics
order by numero_estacion, hora
  );
  