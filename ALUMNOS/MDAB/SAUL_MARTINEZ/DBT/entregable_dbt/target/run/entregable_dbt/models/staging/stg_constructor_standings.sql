
  
  create view "dev"."main"."stg_constructor_standings__dbt_tmp" as (
    with source as (
    select * from "dev"."main"."constructor_standings"
),

renamed as (
    select
        constructor_id,
        cast(season as integer) as season,
        cast(round as integer) as round,
        cast(position as integer) as position,
        cast(points as double) as points,
        cast(wins as integer) as wins
    from source
)

select * from renamed
  );
