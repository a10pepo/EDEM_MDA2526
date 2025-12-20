{% snapshot snapshot__ranked_countries_medals %}

{{
    config(
      target_schema='snapshots',
      unique_key='country',   
      strategy='check',
      check_cols='all',            
      invalidate_hard_deletes=True
    )
}}

-- Asegúrate de que este ref coincida con el nombre de tu modelo final
select * from {{ ref('final__ranked_countries_medals') }}

{% endsnapshot %}