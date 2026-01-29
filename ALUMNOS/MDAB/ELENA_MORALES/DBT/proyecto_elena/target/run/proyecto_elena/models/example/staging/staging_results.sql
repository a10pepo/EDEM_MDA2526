
  
  create view "dev"."main"."staging_results__dbt_tmp" as (
    with source as (
    select * from "dev"."main"."results"
),
renamed as (
    select
        cast("date" as date) as match_date,
        home_team,
        away_team,
        home_score,
        away_score,
        tournament,
        city,
        country,
        neutral
    from source
)
select * from renamed
  );
