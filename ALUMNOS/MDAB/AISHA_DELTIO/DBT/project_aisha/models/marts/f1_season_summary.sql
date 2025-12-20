with race_results as (
    select * from {{ ref('int_f1_race_results') }}
),

metrics as (
    select
        temporada,
        escuderia,
        piloto,
        nacionalidad_piloto,
        
        -- Métricas Básicas
        count(distinct id_unico_resultado) as carreras_disputadas,
        sum(puntos) as puntos_totales,
        sum(es_victoria) as victorias,
        sum(es_podio) as podios,
        
        -- Métricas de Fiabilidad
        sum(case when categoria_resultado = 'Mechanical Failure' then 1 else 0 end) as fallos_mecanicos,
        sum(case when categoria_resultado = 'Accident' then 1 else 0 end) as accidentes_piloto,
        
        -- NUEVA COLUMNA: Porcentaje de Fiabilidad (Carreras sin fallo mecánico)
        round(
            count(distinct case when categoria_resultado != 'Mechanical Failure' then id_unico_resultado end) * 100.0 
            / count(distinct id_unico_resultado), 2
        ) as porcentaje_fiabilidad_mecanica,
        
        -- Cálculo de efectividad
        round(sum(puntos) / count(distinct id_unico_resultado), 2) as media_puntos_por_carrera

    from race_results
    group by temporada, escuderia, piloto, nacionalidad_piloto
),

final_ranking as (
    select
        *,
        -- WINDOW FUNCTIONS
        rank() over (partition by temporada order by puntos_totales desc) as posicion_campeonato,
        rank() over (partition by temporada, escuderia order by puntos_totales desc) as ranking_interno_equipo
    from metrics
)

select * from final_ranking
order by temporada desc, puntos_totales desc