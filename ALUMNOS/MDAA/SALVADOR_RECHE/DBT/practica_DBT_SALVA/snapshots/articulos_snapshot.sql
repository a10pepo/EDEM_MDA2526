{% snapshot articulos_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='articulo_id',
      strategy='check',
      check_cols=['precio_venta', 'coste_compra', 'gama', 'categoria'],
      invalidate_hard_deletes=True
    )
}}

-- Selecciona la fuente a monitorear
select
    articulo_id,
    nombre,
    precio_venta,
    coste_compra,
    gama,
    categoria
from {{ ref('staging__articulos') }}

{% endsnapshot %}