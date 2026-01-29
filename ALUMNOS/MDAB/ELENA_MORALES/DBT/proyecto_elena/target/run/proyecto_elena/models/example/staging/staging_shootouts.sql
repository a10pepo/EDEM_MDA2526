
  
  create view "dev"."main"."staging_shootouts__dbt_tmp" as (
    with source as (
    select * from "dev"."main"."shootouts"
),
renamed as (
    select
        cast("date" as date) as match_date,
        home_team,
        away_team,
        winner
    from source
)
select * from renamed
  );
