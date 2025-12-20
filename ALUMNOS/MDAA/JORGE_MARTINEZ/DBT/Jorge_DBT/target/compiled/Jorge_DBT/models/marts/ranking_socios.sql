with socios as (
    select * from "dev"."main"."stg_socios"
),
ventas as (
    select * from "dev"."main"."stg_ventas"
),
productos as (
    select * from "dev"."main"."stg_productos"
),
metricas_socio as (
    select
        v.socio_id,
        count(distinct v.venta_id) as num_compras,
        sum(v.cantidad * p.precio_venta) as total_gastado_euros
    from ventas v
    join productos p using (producto_id)
    where v.estado = 'completado'
    group by 1
)
select
    s.socio_id,
    s.nombre,
    s.equipo_favorito,
    coalesce(m.total_gastado_euros, 0) as gasto_total,
    case 
        when m.total_gastado_euros > 200 then 'Super VIP'
        when m.total_gastado_euros > 100 then 'VIP'
        else 'Standard'
    end as clasificacion_actual
from socios s
left join metricas_socio m using (socio_id)
order by gasto_total desc