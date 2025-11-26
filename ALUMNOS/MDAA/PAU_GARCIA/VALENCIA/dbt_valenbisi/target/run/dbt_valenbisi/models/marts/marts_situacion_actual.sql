
  
    

  create  table "valenbisi_db"."public"."marts_situacion_actual__dbt_tmp"
  
  
    as
  
  (
    with last_update as (
    select *
    from "valenbisi_db"."public"."int_last_update"
),

ocupacion as (
    select *
    from "valenbisi_db"."public"."int_ocupacion"
),

estado_actual as (
    select
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
        l.momento_medicion,
        l.fecha_medicion,
        l.hora_medicion
    from last_update l
    join ocupacion o
    on l.numero_estacion = o.numero_estacion
    and l.momento_medicion = o.momento_medicion
)

select *
from estado_actual
order by numero_estacion
  );
  