{{ config(materialized='table') }}

with clientes as (
    -- Fuente de la dimensión (datos limpios del cliente)
    select 
        cliente_id, 
        nombre, 
        municipio, 
        modalidad_favorita, 
        -- ¡ATENCIÓN! ELIMINAMOS 'perfil_compra' DE LA SELECCIÓN INICIAL
        fecha_alta
    from {{ ref('staging__clientes') }}
),

ventas_base as (
    -- Traemos el detalle de cada transacción con sus métricas financieras
    select 
        ticket_id, 
        cliente_id, 
        fecha_venta, 
        ingreso_venta, 
        beneficio_neto 
    from {{ ref('intermediate__ventas_con_margen') }}
),

revenue_agregado as (
    -- AGREGACIÓN A NIVEL CLIENTE
    select
        cliente_id,
        count(distinct ticket_id) as total_pedidos,
        sum(ingreso_venta) as facturacion_bruta,
        sum(beneficio_neto) as beneficio_total_cliente,
        min(fecha_venta) as primera_compra_fecha,
        max(fecha_venta) as ultima_compra_fecha
    from ventas_base
    group by 1
)

select
    c.cliente_id,
    c.nombre,
    c.municipio,
    c.modalidad_favorita,
    -- ELIMINAMOS EL ALIAS ROTO: c.perfil_compra as segmento_cliente,
    c.fecha_alta,
    
    -- Métricas de Valor y Frecuencia (del CTE de agregación 'r')
    coalesce(r.total_pedidos, 0) as total_pedidos,
    coalesce(r.facturacion_bruta, 0) as facturacion_total_bruta,
    coalesce(r.beneficio_total_cliente, 0) as beneficio_total_cliente,
    
    r.primera_compra_fecha,
    r.ultima_compra_fecha,
    
    -- KPI de Recencia (Días desde la última compra)
    date_diff('day', r.ultima_compra_fecha, current_date) as dias_desde_ultima_compra_kpi

from clientes c
left join revenue_agregado r on c.cliente_id = r.cliente_id
order by dias_desde_ultima_compra_kpi asc