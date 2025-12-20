with source as (
    select * from {{ source('f1_raw', 'raw_results') }}
),

renamed as (
    select
        resultId as result_id,
        raceId as race_id,
        driverId as driver_id,
        constructorId as constructor_id,
        number as numero_coche,
        grid as posicion_parrilla,
        positionOrder as posicion_final,
        points as puntos,
        laps as vueltas_completadas,
        time as tiempo_total,
        milliseconds as tiempo_milisegundos,
        fastestLap as vuelta_rapida_num,
        rank as ranking_vuelta_rapida,
        fastestLapTime as tiempo_vuelta_rapida,
        fastestLapSpeed as velocidad_media_vuelta_rapida,
        statusId as status_id  
    from source
)

select * from renamed