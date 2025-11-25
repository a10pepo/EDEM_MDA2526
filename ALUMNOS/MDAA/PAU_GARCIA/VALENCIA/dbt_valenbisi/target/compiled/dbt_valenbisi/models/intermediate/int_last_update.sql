with base as (

    -- Partimos del staging
    select *
    from "valenbisi_db"."public"."staging_valenbisi"

),

ordered as (

    select
        *,
        row_number() over (
            partition by numero_estacion
            order by momento_medicion desc
        ) as rn
    from base
),

last_update as (

    -- Nos quedamos solo con la última medición de cada estación
    select
        id,
        numero_estacion,
        nombre_estacion,
        latitud,
        longitud,
        bicicletas_disponibles,
        huecos_disponibles,
        estado_estacion,
        capacidad_total,
        fecha_medicion,
        hora_medicion,
        momento_medicion,
        ultima_consulta
    from ordered
    where rn = 1
)

select *
from last_update