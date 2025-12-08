with race_results as (
    select * from {{ ref('int_f1_race_results') }}
),

career_stats as (
    select
        piloto,
        nacionalidad_piloto,
        -- Lista de equipos por los que ha pasado (agregación de string)
        string_agg(distinct escuderia, ', ') as equipos_historicos,
        
        min(temporada) as temporada_debut,
        max(temporada) as ultima_temporada,
        
        count(*) as total_carreras,
        sum(es_victoria) as total_victorias,
        sum(es_podio) as total_podios,
        sum(puntos) as total_puntos,
        
        -- % de Victorias (Eficiencia)
        round((sum(es_victoria) * 100.0 / count(*)), 2) as porcentaje_victorias

    from race_results
    group by piloto, nacionalidad_piloto
)

select * from career_stats
-- Filtramos para quitar pilotos que solo corrieron 1 vez
where total_carreras > 10
order by total_victorias desc