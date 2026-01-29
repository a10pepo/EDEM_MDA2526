
  
  create view "dev"."main"."finanzas_por_marca__dbt_tmp" as (
    with ventas as (
    select * from "dev"."main"."stg_ventas"
),
productos as (
    select * from "dev"."main"."stg_productos"
),
joined as (
    select
        p.marca,
        p.categoria,
        sum(v.cantidad) as total_unidades_vendidas,
        sum(v.cantidad * p.precio_venta) as facturacion_total,
        sum(v.cantidad * p.beneficio_unitario) as beneficio_total
    from ventas v
    join productos p using (producto_id)
    where v.estado = 'completado' -- Filtramos devoluciones
    group by 1, 2
)
select * from joined
order by facturacion_total desc
  );
