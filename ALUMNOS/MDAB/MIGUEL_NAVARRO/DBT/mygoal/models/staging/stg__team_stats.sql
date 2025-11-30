with source as (

    select * from {{ source('mygoal_raw', 'teamStats') }}

),

renamed as (
    select
        -- Identifiers (fixture, team)
        seasonType          as season_type_id,
        eventId             as fixture_id,
        teamId              as team_id,
        teamOrder           as team_side,
        -- Possession
        possessionPct       as possession_percentage,
        -- Discipline
        foulsCommitted      as fouls_committed,
        yellowCards         as yellow_cards,
        redCards            as red_cards,
        offsides            as offsides_committed,
        wonCorners          as corners_won,
        -- Goalkeeper
        saves               as saves_goalkeeper,
        -- Shoots & Penalties
        totalShots          as shots_total,
        shotsOnTarget       as shots_on_target,
        shotPct * 100       as shot_accuracy,
        penaltyKickGoals    as penalties_scored,
        penaltyKickShots    as penalties_taken,
        -- Passes
        accuratePasses      as passes_completed,
        totalPasses         as passes_total,
        passPct * 100       as pass_accuracy,
        -- Crossing
        accurateCrosses     as crosses_completed,
        totalCrosses        as crosses_total,
        crossPct * 100      as crosses_accuracy,
        -- Long Balls
        totalLongBalls      as long_balls_total,
        accurateLongBalls   as long_balls_completed,
        longballPct * 100   as long_ball_accuracy,
        -- Defense
        blockedShots        as shots_blocked,
        effectiveTackles    as tackles_won,
        totalTackles        as tackles_total,
        tacklePct * 100     as tackle_success_percentage,
        interceptions       as interceptions,
        effectiveClearance  as clearances_effective,
        totalClearance      as clearances_total,
        -- Metadata
        updateTime          as updated_at
    
    from source
)

select * from renamed
