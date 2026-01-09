{{ config(materialized='view') }}

with ventas_enriquecidas as (
    -- Traemos el detalle de la venta (artículo, fecha, cantidad)
    select * from {{ ref('intermediate__ventas_con_margen') }}
),

clientes as (
    -- Traemos la modalidad preferida del cliente
    select 
        cliente_id,
        modalidad_favorita 
    from {{ ref('staging__clientes') }}
)

select
    -- Dimensiones de Agrupación
    extract(quarter from v.fecha_venta) as trimestre_venta,
    v.categoria as tipo_senuelo, -- 'Eging', 'Spinning', 'Jigging', etc.
    c.modalidad_favorita, -- 'Costa', 'Barco', etc.
    
    -- Métricas Agregadas
    sum(v.cantidad) as total_unidades_vendidas,
    sum(v.ingreso_venta) as total_ingreso,
    sum(v.beneficio_neto) as total_beneficio,
    
    -- Margen promedio para este combo (Trimestre + Señuelo + Modalidad)
    round(sum(v.beneficio_neto) / nullif(sum(v.ingreso_venta), 0) * 100, 2) as margen_porcentaje_promedio

from ventas_enriquecidas v
join clientes c on v.cliente_id = c.cliente_id -- JOIN interno, ya que solo analizamos clientes conocidos
group by 1, 2, 3
order by trimestre_venta, total_unidades_vendidas desc