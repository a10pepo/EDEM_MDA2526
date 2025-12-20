{% snapshot snp_drivers %}

{{
    config(
      target_schema='snapshots',
      unique_key='driver_id',
      strategy='check',
      check_cols=['givenName', 'familyName', 'nationality']
    )
}}

select * from {{ ref('drivers') }}

{% endsnapshot %}