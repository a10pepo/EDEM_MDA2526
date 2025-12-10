{% snapshot snapshots__products_snapshot %}

{{
    config(
      unique_key='sku',
      strategy='check',
      check_cols='all'
    )
}}

select * from {{ source('raw', 'products') }}

{% endsnapshot %}
