{% snapshot snapshot_classic %}

{{
    config(
      target_schema='snapshots',
      unique_key='contest_id',
      strategy='check',
      check_cols=['Year'],    
      invalidate_hard_deletes=True
    )
}}

select * from {{ ref('staging__classic') }}

{% endsnapshot %}

{% snapshot snapshot_open %}

{{
    config(
      target_schema='snapshots',
      unique_key='contest_id',
      strategy='check',
      check_cols=['Year'],
      invalidate_hard_deletes=True
    )
}}

select * from {{ ref('staging__open') }}

{% endsnapshot %}

{% snapshot snapshot_212 %}

{{
    config(
      target_schema='snapshots',
      unique_key='contest_id',
      strategy='check',
      check_cols=['Year'],
      invalidate_hard_deletes=True
    )
}}

select * from {{ ref('staging__212') }}

{% endsnapshot %}

{% snapshot snapshot_mens %}

{{
    config(
      target_schema='snapshots',
      unique_key='contest_id',
      strategy='check',
      check_cols=['Year'],
      invalidate_hard_deletes=True
    )
}}

select * from {{ ref('staging__mens') }}

{% endsnapshot %}