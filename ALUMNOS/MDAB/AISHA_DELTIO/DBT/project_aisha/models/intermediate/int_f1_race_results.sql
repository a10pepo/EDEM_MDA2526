with results as (
    select * from {{ ref('stg_f1_results') }}
),

races as (
    select * from {{ ref('stg_f1_races') }}
),

drivers as (
    select * from {{ ref('stg_f1_drivers') }}
),

constructors as (
    select * from {{ ref('stg_f1_constructors') }}
),

status as (
    select * from {{ ref('stg_f1_status') }}
),

joined as (
    select
        -- Identificadores (Usamos nuestra macro de clave subrogada para ser PROs)
        {{ dbt_utils.generate_surrogate_key(['r.race_id', 'd.driver_id']) }} as id_unico_resultado,
        r.temporada,
        r.nombre_gran_premio,
        r.fecha_carrera,
        
        -- Datos del Piloto y Equipo
        d.nombre_completo as piloto,
        d.nacionalidad as nacionalidad_piloto,
        c.nombre_escuderia as escuderia,
        
        -- Resultados Numéricos
        res.posicion_parrilla,
        res.posicion_final,
        res.puntos,
        res.vueltas_completadas,
        res.tiempo_vuelta_rapida,
        
        -- KPIs Calculados (Usando Macros)
        {{ is_victory('res.posicion_final') }} as es_victoria,
        {{ is_podium('res.posicion_final') }} as es_podio,
        {{ is_in_points('res.posicion_final') }} as es_zona_puntos,
        
        -- Análisis de Fiabilidad (Macro get_race_outcome)
        s.descripcion_estado,
        {{ get_race_outcome('s.descripcion_estado') }} as categoria_resultado,
        
        -- Bandera simple para saber si terminó o no
        case 
            when {{ get_race_outcome('s.descripcion_estado') }} = 'Finished' then 1 
            else 0 
        end as termino_carrera

    from results res
    left join races r on res.race_id = r.race_id
    left join drivers d on res.driver_id = d.driver_id
    left join constructors c on res.constructor_id = c.constructor_id
    left join status s on res.status_id = s.status_id
)

select * from joined