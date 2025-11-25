
  create view "valenbisi_db"."public"."int_evolucion_temporal__dbt_tmp"
    
    
  as (
    with base as (

    select *
    from "valenbisi_db"."public"."staging_valenbisi"

),

evolucion as (

    select
        id,
        numero_estacion,
        nombre_estacion,
        bicicletas_disponibles,
        huecos_disponibles,
        capacidad_total,
        momento_medicion,

        bicicletas_disponibles 
            - lag(bicicletas_disponibles) over (
                partition by numero_estacion 
                order by momento_medicion
            ) as variacion_bicis,

        huecos_disponibles
            - lag(huecos_disponibles) over (
                partition by numero_estacion 
                order by momento_medicion
            ) as variacion_huecos,

        momento_medicion
            - lag(momento_medicion) over (
                partition by numero_estacion 
                order by momento_medicion
            ) as tiempo_desde_ultima_actualizacion

    from base
)

select * from evolucion
  );