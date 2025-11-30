with source as (

    select * from {{ source('mygoal_raw', 'leagues') }}

),

renamed as (
    select
        seasonType          as season_type_id,
        year                as season_start_year,
        seasonName          as season_name,
        seasonSlug          as season_slug,
        leagueId            as league_id,
        midsizeName         as league_code,
        leagueName          as league_name,
        leagueShortName     as league_short_name
    
    from source
)

select * from renamed