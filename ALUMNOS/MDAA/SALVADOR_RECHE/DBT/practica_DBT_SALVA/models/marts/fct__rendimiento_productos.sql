{{ config(materialized='table') }}

with ventas_enriquecidas as (
    -- Datos financieros agregados
    select
        articulo_id,
        nombre_articulo,
        categoria,
        gama,
        sum(cantidad) as unidades_vendidas,
        sum(ingreso_venta) as facturacion_total,
        sum(beneficio_neto) as beneficio_total
    from {{ ref('intermediate__ventas_con_margen') }}
    group by 1, 2, 3, 4
),

stats_pesca as (
    -- Métricas de pesca (Total Capturas, Peso Promedio, etc.)
    select * from {{ ref('intermediate__estadisticas_pesca') }}
),

productos_unidos as (
    select
        v.*,
        p.total_capturas_registradas,
        p.record_peso_kg,
        p.especies_objetivo
    from ventas_enriquecidas v
    left join stats_pesca p on v.articulo_id = p.articulo_id
)

select
    -- Dimensiones
    articulo_id,
    nombre_articulo,
    categoria,
    gama,
    
    -- Métricas de Negocio
    unidades_vendidas,
    facturacion_total,
    beneficio_total,
    
    -- Métricas de Eficacia
    coalesce(total_capturas_registradas, 0) as capturas_totales,
    especies_objetivo,
    record_peso_kg,
    
    -- KPI: RANKING DE LOS 'KILLER LURES' (El modelo que más peces saca es el 1)
    rank() over (order by coalesce(total_capturas_registradas, 0) desc) as ranking_capturas_global,
    
    -- KPI: Ratio de Capturas por Unidad Vendida
    case 
        when unidades_vendidas > 0 
        then round(coalesce(total_capturas_registradas, 0) / unidades_vendidas::float, 2)
        else 0 
    end as ratio_efectividad_real

from productos_unidos
order by ranking_capturas_global asc