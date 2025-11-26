with base as (
    select *
    from {{ ref('staging_valenbisi') }}
),

last_update as (
    select distinct on (numero_estacion)
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
    from base
    order by numero_estacion, momento_medicion desc
)

select *
from last_update
