{{ config(materialized='view') }}

with ventas as (
    select * from {{ ref('staging__ventas') }}
),

articulos as (
    select * from {{ ref('staging__articulos') }}
)

select
    v.ticket_id,
    v.fecha_venta,
    v.cliente_id,
    v.articulo_id,
    ar.nombre as nombre_articulo,
    ar.categoria,
    ar.gama,
    
    v.cantidad,
    
    -- CORRECCIÓN DE LÓGICA DE NEGOCIO:
    -- Como el CSV de ventas tiene el precio unitario en la columna 'total',
    -- recalculamos el ingreso real multiplicando por cantidad.
    (v.cantidad * ar.precio_venta) as ingreso_venta,
    
    -- Beneficio Neto: ¡USANDO LA MACRO!
    -- La macro toma los ALIASES que definiste (v. y ar.) como argumentos.
    {{ calcular_beneficio_neto(
        'v.cantidad', 
        'ar.precio_venta', 
        'ar.coste_compra') }} as beneficio_neto,
        
    -- Margen porcentual (depende del beneficio_neto que acabamos de calcular)
    round(
        {{ calcular_beneficio_neto('v.cantidad', 'ar.precio_venta', 'ar.coste_compra') }} 
        / nullif((v.cantidad * ar.precio_venta), 0) * 100, 
    2) as margen_porcentaje

from ventas v
left join articulos ar on v.articulo_id = ar.articulo_id