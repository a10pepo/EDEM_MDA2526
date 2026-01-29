{% snapshot snapshot_league_table %}

{{
    config(
      target_schema='snapshots',
      unique_key='dbt_scd_id', 
      strategy='check',
      check_cols=['points', 'gamesPlayed', 'teamRank'],
    )
}}

select 
    *,
    -- Creo la clave única usando los IDs principales y casteando a texto:
    cast(seasonType as varchar) || '-' || cast(teamId as varchar) as dbt_scd_id 
from {{ source('mygoal_raw', 'standings') }}

{% endsnapshot %}