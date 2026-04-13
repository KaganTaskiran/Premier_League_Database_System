-- ============================================================
-- Premier League Data Management System - Analytical Queries
-- SE 2230: Database Systems - Yaşar University 2026
-- 10 Season Coverage: 2015/16 → 2024/25
-- ============================================================

USE premier_league_db;

-- ============================================================
-- QUERY 1: All-time Champion Teams (Most titles won)
-- ============================================================
SELECT
    c.name                              AS club,
    COUNT(*)                            AS titles,
    GROUP_CONCAT(ls.season ORDER BY ls.season SEPARATOR ', ') AS winning_seasons
FROM LeagueStandings ls
JOIN Club c ON ls.club_id = c.club_id
WHERE (ls.won * 3 + ls.drawn) = (
    SELECT MAX(won * 3 + drawn)
    FROM LeagueStandings ls2
    WHERE ls2.season = ls.season
)
GROUP BY c.club_id
ORDER BY titles DESC;

-- ============================================================
-- QUERY 2: Season-by-Season Champions with Points (using Subquery)
-- ============================================================
SELECT
    ls.season,
    c.name                          AS champion,
    ls.won, ls.drawn, ls.lost,
    ls.goals_for                    AS gf,
    ls.goals_against                AS ga,
    (ls.goals_for - ls.goals_against)  AS gd,
    (ls.won * 3 + ls.drawn)        AS points
FROM LeagueStandings ls
JOIN Club c ON ls.club_id = c.club_id
WHERE (ls.won * 3 + ls.drawn) = (
    SELECT MAX(won * 3 + drawn)
    FROM LeagueStandings ls2
    WHERE ls2.season = ls.season
)
ORDER BY ls.season;

-- ============================================================
-- QUERY 3: League Table for a Specific Season (VIEW usage)
-- Change '2024/25' to any season to see that table
-- ============================================================
SELECT * FROM v_league_table
WHERE season = '2024/25'
ORDER BY points DESC, gd DESC;

-- Show all seasons:
SELECT * FROM v_league_table
WHERE season = '2023/24'
ORDER BY points DESC, gd DESC;

SELECT * FROM v_league_table
WHERE season = '2015/16'
ORDER BY points DESC, gd DESC;

-- ============================================================
-- QUERY 4: Top Scorers Per Season (Multi-table JOIN + Aggregate)
-- ============================================================
SELECT
    m.season,
    CONCAT(p.first_name, ' ', p.last_name)  AS player,
    c.name                                   AS club,
    SUM(ps.goals)                            AS goals,
    SUM(ps.assists)                          AS assists,
    COUNT(ps.match_id)                       AS matches_played
FROM PlayerStatistics ps
JOIN Player  p ON ps.player_id = p.player_id
JOIN `Match` m ON ps.match_id  = m.match_id
JOIN Club    c ON p.club_id    = c.club_id
GROUP BY p.player_id, m.season
HAVING SUM(ps.goals) = (
    SELECT MAX(sub.total)
    FROM (
        SELECT ps2.player_id, m2.season, SUM(ps2.goals) AS total
        FROM PlayerStatistics ps2
        JOIN `Match` m2 ON ps2.match_id = m2.match_id
        GROUP BY ps2.player_id, m2.season
    ) sub
    WHERE sub.season = m.season
)
ORDER BY m.season;

-- ============================================================
-- QUERY 5: All-Time Top Scorers (Across All 10 Seasons)
-- ============================================================
SELECT
    CONCAT(p.first_name, ' ', p.last_name)  AS player,
    p.nationality,
    p.position,
    COALESCE(c.name, 'N/A (Left PL)')       AS current_club,
    SUM(ps.goals)                            AS total_goals,
    SUM(ps.assists)                          AS total_assists,
    COUNT(DISTINCT m.season)                 AS seasons_played,
    COUNT(ps.match_id)                       AS total_matches,
    ROUND(SUM(ps.goals) / COUNT(ps.match_id), 2) AS goals_per_game
FROM PlayerStatistics ps
JOIN Player  p ON ps.player_id = p.player_id
JOIN `Match` m ON ps.match_id  = m.match_id
LEFT JOIN Club c ON p.club_id  = c.club_id
GROUP BY p.player_id
ORDER BY total_goals DESC
LIMIT 15;

-- ============================================================
-- QUERY 6: Club Performance Over 10 Seasons
-- Total points, wins, goals across all seasons
-- ============================================================
SELECT
    c.name                              AS club,
    COUNT(DISTINCT ls.season)           AS seasons_in_data,
    SUM(ls.played)                      AS total_played,
    SUM(ls.won)                         AS total_wins,
    SUM(ls.drawn)                       AS total_draws,
    SUM(ls.lost)                        AS total_losses,
    SUM(ls.goals_for)                   AS total_goals_scored,
    SUM(ls.goals_against)               AS total_goals_conceded,
    SUM(ls.won * 3 + ls.drawn)          AS total_points,
    ROUND(SUM(ls.won) * 100.0 / SUM(ls.played), 1) AS win_percentage
FROM LeagueStandings ls
JOIN Club c ON ls.club_id = c.club_id
GROUP BY c.club_id
ORDER BY total_points DESC;

-- ============================================================
-- QUERY 7: Best Single Seasons in History (Top Points)
-- ============================================================
SELECT
    ls.season,
    c.name                              AS club,
    ls.played, ls.won, ls.drawn, ls.lost,
    ls.goals_for, ls.goals_against,
    (ls.goals_for - ls.goals_against)   AS gd,
    (ls.won * 3 + ls.drawn)             AS points
FROM LeagueStandings ls
JOIN Club c ON ls.club_id = c.club_id
ORDER BY points DESC
LIMIT 10;

-- ============================================================
-- QUERY 8: Head-to-Head Record Between Arsenal and Liverpool
-- ============================================================
CALL sp_head_to_head(1, 3);

-- Head-to-head Man City vs Man United:
CALL sp_head_to_head(4, 5);

-- ============================================================
-- QUERY 9: Player Career Stats (Window Function + Subquery)
-- Rank players by goals within each season
-- ============================================================
SELECT
    season,
    player,
    club,
    goals,
    assists,
    RANK() OVER (PARTITION BY season ORDER BY goals DESC) AS season_rank
FROM v_top_scorers
WHERE goals > 0
ORDER BY season DESC, season_rank;

-- ============================================================
-- QUERY 10: Transfer Market Analysis - Most Expensive Signings
-- ============================================================
SELECT
    CONCAT(p.first_name, ' ', p.last_name)  AS player,
    p.position,
    COALESCE(fc.name, 'Free Agent / Academy') AS from_club,
    tc.name                                   AS to_club,
    t.season,
    t.transfer_fee                            AS fee_M,
    t.transfer_date
FROM Transfer t
JOIN Player   p  ON t.player_id    = p.player_id
LEFT JOIN Club fc ON t.from_club_id = fc.club_id
JOIN Club     tc ON t.to_club_id   = tc.club_id
WHERE t.transfer_fee IS NOT NULL
ORDER BY t.transfer_fee DESC
LIMIT 15;

-- ============================================================
-- QUERY 11: Average Market Value vs Performance
-- Clubs with best points-per-million-euro ratio
-- ============================================================
SELECT
    c.name                          AS club,
    ROUND(SUM(p.market_value), 1)   AS squad_value_M,
    SUM(ls.won * 3 + ls.drawn)      AS points_2024_25,
    ROUND(SUM(ls.won * 3 + ls.drawn) / SUM(p.market_value), 3) AS pts_per_million
FROM Player p
JOIN Club c ON p.club_id = c.club_id
JOIN LeagueStandings ls ON ls.club_id = c.club_id AND ls.season = '2024/25'
WHERE p.market_value IS NOT NULL
GROUP BY c.club_id
ORDER BY pts_per_million DESC;

-- ============================================================
-- QUERY 12: Clubs with Most Injuries (All Time)
-- ============================================================
SELECT
    c.name                      AS club,
    COUNT(i.injury_id)          AS total_injuries,
    SUM(i.matches_missed)       AS total_matches_missed,
    ROUND(AVG(i.matches_missed),1) AS avg_matches_missed,
    COUNT(CASE WHEN i.end_date IS NULL OR i.end_date >= CURDATE()
               THEN 1 END)      AS currently_injured
FROM Injury i
JOIN Player p ON i.player_id = p.player_id
JOIN Club   c ON p.club_id   = c.club_id
GROUP BY c.club_id
ORDER BY total_injuries DESC;

-- ============================================================
-- QUERY 13: Season Trends - Goals Scored Per Season
-- (Which era had the most goals?)
-- ============================================================
SELECT
    m.season,
    COUNT(m.match_id)                        AS matches_played,
    SUM(m.home_score + m.away_score)         AS total_goals,
    ROUND(SUM(m.home_score + m.away_score) / COUNT(m.match_id), 2) AS goals_per_match,
    MAX(m.home_score + m.away_score)         AS highest_scoring_match
FROM `Match` m
GROUP BY m.season
ORDER BY m.season;

-- ============================================================
-- QUERY 14: Player Nationality Diversity by Club
-- ============================================================
SELECT
    c.name                              AS club,
    COUNT(DISTINCT p.nationality)       AS nationalities,
    COUNT(p.player_id)                  AS squad_size,
    GROUP_CONCAT(DISTINCT p.nationality ORDER BY p.nationality SEPARATOR ', ') AS countries
FROM Player p
JOIN Club c ON p.club_id = c.club_id
GROUP BY c.club_id
ORDER BY nationalities DESC;

-- ============================================================
-- QUERY 15: Comeback Kings - Clubs with Best Away Record
-- ============================================================
SELECT
    c.name                  AS club,
    COUNT(*)                AS away_matches,
    SUM(CASE WHEN m.away_score > m.home_score THEN 1 ELSE 0 END) AS away_wins,
    SUM(CASE WHEN m.away_score = m.home_score THEN 1 ELSE 0 END) AS away_draws,
    SUM(CASE WHEN m.away_score < m.home_score THEN 1 ELSE 0 END) AS away_losses,
    ROUND(SUM(CASE WHEN m.away_score > m.home_score THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS away_win_pct,
    SUM(m.away_score)       AS goals_scored_away
FROM `Match` m
JOIN Club c ON m.away_club_id = c.club_id
GROUP BY c.club_id
HAVING away_matches >= 3
ORDER BY away_win_pct DESC;

-- ============================================================
-- QUERY 16: Stored Procedure - Player Season Stats
-- ============================================================
CALL sp_player_season_stats(9,  '2017/18');   -- Salah's record-breaking season
CALL sp_player_season_stats(13, '2022/23');   -- Haaland's record-breaking season
CALL sp_player_season_stats(62, '2015/16');   -- Vardy's title-winning season

-- ============================================================
-- QUERY 17: 10-Season League Performance Ranking (RANK Window)
-- ============================================================
SELECT
    c.name                                  AS club,
    SUM(ls.won * 3 + ls.drawn)             AS decade_points,
    SUM(ls.won)                             AS decade_wins,
    SUM(ls.goals_for)                       AS decade_goals,
    RANK() OVER (ORDER BY SUM(ls.won * 3 + ls.drawn) DESC) AS decade_rank
FROM LeagueStandings ls
JOIN Club c ON ls.club_id = c.club_id
GROUP BY c.club_id
ORDER BY decade_points DESC;
