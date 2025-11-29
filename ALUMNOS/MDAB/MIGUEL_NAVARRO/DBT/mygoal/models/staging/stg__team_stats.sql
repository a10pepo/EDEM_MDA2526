with source as (

    select * from {{ source('mygoal_raw', 'teamStats') }}

)

renamed as (
    select
        -- Identifiers
        seasonType          as season_type_id,
        eventId             as fixture_id,
        teamId              as team_id,
        teamOrder           as team_side,
        possessionPct       as possession_percentage,
        foulsCommitted      as fouls_committed,
        yellowCards         as yellow_cards,
        redCards            as red_cards,
        offsides            as offsides_committed,
        wonCorners          as corners_won,
        saves               as saves_goalkeeper,
        totalShots          as shots_total,
        shotsOnTarget       as shots_on_target,
        shotPct             as shot_accuracy,
        penaltyKickGoals    as penalties_scored,
        penaltyKickShots    as penalties_taken,
        accuratePasses      as passes_completed,
        totalPasses         as total_passes,
        passPct             as pass_percentage,
        -- Crossing
        accurateCrosses     as crosses_completed,
        totalCrosses        as crosses_total,
        crossPct            as crosses_accuracy,totalLongBalls,accurateLongBalls,longballPct,
        blockedShots        as shots_blocked,
        effectiveTackles,totalTackles,tacklePct,interceptions,effectiveClearance,totalClearance,
        updateTime          as updated_at
    
    from source

)

select * from renamed
