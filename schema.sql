-- ============================================================
-- Premier League Data Management System
-- SE 2230: Database Systems - Term Project
-- Yaşar University, 2026
-- Group: Kağan Taşkıran, Cem Arda Budak, Berker Vergi
-- ============================================================

DROP DATABASE IF EXISTS premier_league_db;
CREATE DATABASE premier_league_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE premier_league_db;

-- ============================================================
-- TABLE: Club
-- ============================================================
CREATE TABLE Club (
    club_id    INT          AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    city       VARCHAR(100) NOT NULL,
    stadium    VARCHAR(100) NOT NULL,
    capacity   INT          CHECK (capacity > 0),
    founded    INT          CHECK (founded BETWEEN 1800 AND 2100),
    CONSTRAINT uq_club_name UNIQUE (name)
);

-- ============================================================
-- TABLE: Coach
-- ============================================================
CREATE TABLE Coach (
    coach_id       INT          AUTO_INCREMENT PRIMARY KEY,
    first_name     VARCHAR(50)  NOT NULL,
    last_name      VARCHAR(50)  NOT NULL,
    nationality    VARCHAR(50),
    date_of_birth  DATE,
    club_id        INT,
    contract_start DATE,
    contract_end   DATE,
    CONSTRAINT fk_coach_club FOREIGN KEY (club_id)
        REFERENCES Club(club_id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================
-- TABLE: Player
-- ============================================================
CREATE TABLE Player (
    player_id      INT          AUTO_INCREMENT PRIMARY KEY,
    first_name     VARCHAR(50)  NOT NULL,
    last_name      VARCHAR(50)  NOT NULL,
    nationality    VARCHAR(50),
    date_of_birth  DATE,
    position       ENUM('Goalkeeper','Defender','Midfielder','Forward') NOT NULL,
    jersey_number  INT          CHECK (jersey_number BETWEEN 1 AND 99),
    club_id        INT,
    market_value   DECIMAL(8,2),  -- millions EUR
    contract_end   DATE,
    CONSTRAINT fk_player_club FOREIGN KEY (club_id)
        REFERENCES Club(club_id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================
-- TABLE: Match
-- ============================================================
CREATE TABLE `Match` (
    match_id     INT          AUTO_INCREMENT PRIMARY KEY,
    home_club_id INT          NOT NULL,
    away_club_id INT          NOT NULL,
    match_date   DATE         NOT NULL,
    home_score   INT          DEFAULT 0 CHECK (home_score >= 0),
    away_score   INT          DEFAULT 0 CHECK (away_score >= 0),
    season       VARCHAR(10)  NOT NULL,
    gameweek     INT          CHECK (gameweek BETWEEN 1 AND 38),
    CONSTRAINT fk_match_home FOREIGN KEY (home_club_id)
        REFERENCES Club(club_id) ON UPDATE CASCADE,
    CONSTRAINT fk_match_away FOREIGN KEY (away_club_id)
        REFERENCES Club(club_id) ON UPDATE CASCADE
    -- chk_teams: aynı kulüp kendisiyle oynayamaz → BEFORE INSERT trigger ile kontrol edilir
);

-- ============================================================
-- TABLE: PlayerStatistics
-- ============================================================
CREATE TABLE PlayerStatistics (
    stat_id          INT AUTO_INCREMENT PRIMARY KEY,
    player_id        INT NOT NULL,
    match_id         INT NOT NULL,
    goals            INT DEFAULT 0 CHECK (goals >= 0),
    assists          INT DEFAULT 0 CHECK (assists >= 0),
    yellow_cards     INT DEFAULT 0 CHECK (yellow_cards IN (0,1,2)),
    red_cards        INT DEFAULT 0 CHECK (red_cards IN (0,1)),
    minutes_played   INT DEFAULT 0 CHECK (minutes_played BETWEEN 0 AND 120),
    shots_on_target  INT DEFAULT 0 CHECK (shots_on_target >= 0),
    passes_completed INT DEFAULT 0 CHECK (passes_completed >= 0),
    CONSTRAINT fk_stat_player  FOREIGN KEY (player_id)
        REFERENCES Player(player_id) ON DELETE CASCADE,
    CONSTRAINT fk_stat_match   FOREIGN KEY (match_id)
        REFERENCES `Match`(match_id)  ON DELETE CASCADE,
    CONSTRAINT uq_player_match UNIQUE (player_id, match_id)
);

-- ============================================================
-- TABLE: Transfer
-- ============================================================
CREATE TABLE Transfer (
    transfer_id   INT          AUTO_INCREMENT PRIMARY KEY,
    player_id     INT          NOT NULL,
    from_club_id  INT,
    to_club_id    INT          NOT NULL,
    transfer_date DATE         NOT NULL,
    transfer_fee  DECIMAL(8,2),  -- millions EUR, NULL = free/loan
    season        VARCHAR(10),
    CONSTRAINT fk_transfer_player FOREIGN KEY (player_id)
        REFERENCES Player(player_id),
    CONSTRAINT fk_transfer_from   FOREIGN KEY (from_club_id)
        REFERENCES Club(club_id),
    CONSTRAINT fk_transfer_to     FOREIGN KEY (to_club_id)
        REFERENCES Club(club_id)
);

-- ============================================================
-- TABLE: Injury
-- ============================================================
CREATE TABLE Injury (
    injury_id      INT          AUTO_INCREMENT PRIMARY KEY,
    player_id      INT          NOT NULL,
    injury_type    VARCHAR(100) NOT NULL,
    start_date     DATE         NOT NULL,
    end_date       DATE,
    matches_missed INT          DEFAULT 0 CHECK (matches_missed >= 0),
    CONSTRAINT fk_injury_player FOREIGN KEY (player_id)
        REFERENCES Player(player_id) ON DELETE CASCADE
);

-- ============================================================
-- TABLE: LeagueStandings
-- ============================================================
CREATE TABLE LeagueStandings (
    standing_id   INT         AUTO_INCREMENT PRIMARY KEY,
    club_id       INT         NOT NULL,
    season        VARCHAR(10) NOT NULL,
    played        INT         DEFAULT 0,
    won           INT         DEFAULT 0,
    drawn         INT         DEFAULT 0,
    lost          INT         DEFAULT 0,
    goals_for     INT         DEFAULT 0,
    goals_against INT         DEFAULT 0,
    CONSTRAINT fk_standing_club FOREIGN KEY (club_id)
        REFERENCES Club(club_id) ON UPDATE CASCADE,
    CONSTRAINT uq_club_season UNIQUE (club_id, season)
);

-- ============================================================
-- VIEWS
-- ============================================================

-- View 1: Full league table with computed columns and ranking
CREATE VIEW v_league_table AS
SELECT
    ls.season,
    RANK() OVER (
        PARTITION BY ls.season
        ORDER BY (ls.won*3 + ls.drawn) DESC,
                 (ls.goals_for - ls.goals_against) DESC,
                 ls.goals_for DESC
    )                                     AS position,
    c.name                                AS club,
    c.stadium,
    ls.played,
    ls.won,
    ls.drawn,
    ls.lost,
    ls.goals_for                          AS gf,
    ls.goals_against                      AS ga,
    (ls.goals_for - ls.goals_against)     AS gd,
    (ls.won * 3 + ls.drawn)               AS points
FROM LeagueStandings ls
JOIN Club c ON ls.club_id = c.club_id;

-- View 2: Top scorers with club and season info
CREATE VIEW v_top_scorers AS
SELECT
    p.player_id,
    CONCAT(p.first_name, ' ', p.last_name) AS player_name,
    p.nationality,
    p.position,
    c.name                                  AS club,
    m.season,
    SUM(ps.goals)                           AS total_goals,
    SUM(ps.assists)                         AS total_assists,
    COUNT(ps.match_id)                      AS matches_played,
    SUM(ps.minutes_played)                  AS total_minutes
FROM PlayerStatistics ps
JOIN Player  p ON ps.player_id = p.player_id
JOIN `Match` m ON ps.match_id  = m.match_id
JOIN Club    c ON p.club_id    = c.club_id
GROUP BY p.player_id, m.season;

-- View 3: Player profile with age and club
CREATE VIEW v_player_profile AS
SELECT
    p.player_id,
    CONCAT(p.first_name, ' ', p.last_name)      AS full_name,
    p.nationality,
    p.position,
    p.jersey_number,
    TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()) AS age,
    c.name                                       AS club,
    c.city,
    p.market_value,
    p.contract_end
FROM Player p
LEFT JOIN Club c ON p.club_id = c.club_id;

-- View 4: Match results with club names and outcome
CREATE VIEW v_match_results AS
SELECT
    m.match_id,
    m.season,
    m.gameweek,
    m.match_date,
    hc.name     AS home_club,
    m.home_score,
    m.away_score,
    ac.name     AS away_club,
    CASE
        WHEN m.home_score > m.away_score THEN hc.name
        WHEN m.away_score > m.home_score THEN ac.name
        ELSE 'Draw'
    END         AS winner
FROM `Match` m
JOIN Club hc ON m.home_club_id = hc.club_id
JOIN Club ac ON m.away_club_id = ac.club_id;

-- View 5: Active injuries
CREATE VIEW v_active_injuries AS
SELECT
    i.injury_id,
    CONCAT(p.first_name, ' ', p.last_name) AS player_name,
    p.position,
    c.name                                  AS club,
    i.injury_type,
    i.start_date,
    i.end_date,
    i.matches_missed,
    DATEDIFF(CURDATE(), i.start_date)       AS days_injured
FROM Injury i
JOIN Player p ON i.player_id = p.player_id
LEFT JOIN Club c ON p.club_id = c.club_id
WHERE i.end_date IS NULL OR i.end_date >= CURDATE();

-- ============================================================
-- STORED PROCEDURES
-- ============================================================

DELIMITER $$

-- Procedure 1: Update league standings after inserting a match result
CREATE PROCEDURE sp_update_standings(IN p_match_id INT)
BEGIN
    DECLARE v_home_id    INT;
    DECLARE v_away_id    INT;
    DECLARE v_home_score INT;
    DECLARE v_away_score INT;
    DECLARE v_season     VARCHAR(10);

    SELECT home_club_id, away_club_id, home_score, away_score, season
    INTO   v_home_id, v_away_id, v_home_score, v_away_score, v_season
    FROM   `Match` WHERE match_id = p_match_id;

    INSERT IGNORE INTO LeagueStandings (club_id, season)
    VALUES (v_home_id, v_season), (v_away_id, v_season);

    -- Home club update
    UPDATE LeagueStandings SET
        played        = played + 1,
        won           = won   + IF(v_home_score > v_away_score, 1, 0),
        drawn         = drawn + IF(v_home_score = v_away_score, 1, 0),
        lost          = lost  + IF(v_home_score < v_away_score, 1, 0),
        goals_for     = goals_for     + v_home_score,
        goals_against = goals_against + v_away_score
    WHERE club_id = v_home_id AND season = v_season;

    -- Away club update
    UPDATE LeagueStandings SET
        played        = played + 1,
        won           = won   + IF(v_away_score > v_home_score, 1, 0),
        drawn         = drawn + IF(v_home_score = v_away_score, 1, 0),
        lost          = lost  + IF(v_away_score < v_home_score, 1, 0),
        goals_for     = goals_for     + v_away_score,
        goals_against = goals_against + v_home_score
    WHERE club_id = v_away_id AND season = v_season;
END$$

-- Procedure 2: Get complete season stats for a player
CREATE PROCEDURE sp_player_season_stats(
    IN p_player_id INT,
    IN p_season    VARCHAR(10)
)
BEGIN
    SELECT
        CONCAT(p.first_name, ' ', p.last_name)           AS player,
        c.name                                            AS club,
        p.position,
        p_season                                          AS season,
        COUNT(ps.match_id)                                AS matches,
        SUM(ps.goals)                                     AS goals,
        SUM(ps.assists)                                   AS assists,
        SUM(ps.yellow_cards)                              AS yellow_cards,
        SUM(ps.red_cards)                                 AS red_cards,
        SUM(ps.minutes_played)                            AS total_minutes,
        SUM(ps.shots_on_target)                           AS shots_on_target,
        ROUND(SUM(ps.goals) / NULLIF(COUNT(ps.match_id),0), 2) AS goals_per_game
    FROM PlayerStatistics ps
    JOIN Player  p ON ps.player_id = p.player_id
    JOIN `Match` m ON ps.match_id  = m.match_id
    JOIN Club    c ON p.club_id    = c.club_id
    WHERE ps.player_id = p_player_id AND m.season = p_season
    GROUP BY ps.player_id;
END$$

-- Procedure 3: Get head-to-head record between two clubs
CREATE PROCEDURE sp_head_to_head(
    IN p_club1_id INT,
    IN p_club2_id INT
)
BEGIN
    SELECT
        m.season,
        m.match_date,
        hc.name     AS home_club,
        m.home_score,
        m.away_score,
        ac.name     AS away_club,
        CASE
            WHEN m.home_score > m.away_score THEN hc.name
            WHEN m.away_score > m.home_score THEN ac.name
            ELSE 'Draw'
        END         AS winner
    FROM `Match` m
    JOIN Club hc ON m.home_club_id = hc.club_id
    JOIN Club ac ON m.away_club_id = ac.club_id
    WHERE (m.home_club_id = p_club1_id AND m.away_club_id = p_club2_id)
       OR (m.home_club_id = p_club2_id AND m.away_club_id = p_club1_id)
    ORDER BY m.match_date DESC;
END$$

DELIMITER ;

-- ============================================================
-- TRIGGERS
-- ============================================================

DELIMITER $$

-- Trigger 1: Automatically update player's club after a transfer
CREATE TRIGGER trg_transfer_update_club
AFTER INSERT ON Transfer
FOR EACH ROW
BEGIN
    UPDATE Player
    SET    club_id = NEW.to_club_id
    WHERE  player_id = NEW.player_id;
END$$

-- Trigger 2: Prevent scheduling a match with a team on the same date
CREATE TRIGGER trg_prevent_double_booking
BEFORE INSERT ON `Match`
FOR EACH ROW
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count
    FROM `Match`
    WHERE match_date = NEW.match_date
      AND (home_club_id IN (NEW.home_club_id, NEW.away_club_id)
        OR away_club_id IN (NEW.home_club_id, NEW.away_club_id));

    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A club already has a match scheduled on this date.';
    END IF;
END$$

DELIMITER ;
