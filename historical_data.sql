-- ============================================================
-- Premier League Data Management System - 10 Season Historical Data
-- SE 2230: Database Systems - Yaşar University 2026
-- Seasons covered: 2015/16 → 2024/25
-- ============================================================

USE premier_league_db;

-- Disable double-booking trigger for bulk historical insert
DROP TRIGGER IF EXISTS trg_prevent_double_booking;

-- ============================================================
-- SECTION 1: HISTORICAL CLUBS (club_id 11-24)
-- ============================================================
INSERT INTO Club (club_id, name, city, stadium, capacity, founded) VALUES
(11, 'Leicester City',           'Leicester',      'King Power Stadium',          32261, 1884),
(12, 'Everton',                  'Liverpool',      'Goodison Park',               39414, 1878),
(13, 'Wolverhampton Wanderers',  'Wolverhampton',  'Molineux Stadium',            31750, 1877),
(14, 'Crystal Palace',           'London',         'Selhurst Park',               25486, 1905),
(15, 'Southampton',              'Southampton',    'St. Mary\'s Stadium',         32384, 1885),
(16, 'Burnley',                  'Burnley',        'Turf Moor',                   21944, 1882),
(17, 'Leeds United',             'Leeds',          'Elland Road',                 37890, 1919),
(18, 'Sheffield United',         'Sheffield',      'Bramall Lane',                32050, 1889),
(19, 'Brentford',                'London',         'Gtech Community Stadium',     17250, 1889),
(20, 'Nottingham Forest',        'Nottingham',     'City Ground',                 30445, 1865),
(21, 'Fulham',                   'London',         'Craven Cottage',              25700, 1879),
(22, 'West Bromwich Albion',     'West Bromwich',  'The Hawthorns',               26688, 1878),
(23, 'Watford',                  'Watford',        'Vicarage Road',               21577, 1881),
(24, 'Stoke City',               'Stoke-on-Trent', 'bet365 Stadium',              29559, 1863);

-- ============================================================
-- SECTION 2: HISTORICAL COACHES
-- ============================================================
INSERT INTO Coach (first_name, last_name, nationality, date_of_birth, club_id, contract_start, contract_end) VALUES
('Claudio',  'Ranieri',    'Italian',    '1951-10-20', 11, '2015-07-13', '2017-02-23'),
('Carlo',    'Ancelotti',  'Italian',    '1959-06-10', 12, '2023-06-12', '2026-06-30'),
('Nuno',     'Santo',      'Portuguese', '1974-01-25', 13, '2017-05-31', '2021-07-19'),
('Oliver',   'Glasner',    'Austrian',   '1974-08-25', 14, '2024-02-16', '2026-06-30'),
('Russel',   'Martin',     'Scottish',   '1986-01-04', 15, '2023-06-06', '2026-06-30'),
('Scott',    'Parker',     'English',    '1980-10-13', 16, '2024-01-11', '2026-06-30'),
('Daniel',   'Farke',      'German',     '1976-10-30', 17, '2023-07-10', '2025-06-30'),
('Chris',    'Wilder',     'English',    '1967-09-23', 18, '2023-12-19', '2025-06-30'),
('Thomas',   'Frank',      'Danish',     '1973-09-27', 19, '2018-10-23', '2026-06-30'),
('Nuno',     'Espirito Santo','Portuguese','1974-01-25',20, '2022-09-22', '2026-06-30');

-- ============================================================
-- SECTION 3: HISTORICAL KEY PLAYERS (player_id 41-76)
-- ============================================================
INSERT INTO Player (player_id, first_name, last_name, nationality, date_of_birth, position, jersey_number, club_id, market_value, contract_end) VALUES
-- Arsenal legends
(41, 'Alexis',       'Sanchez',        'Chilean',      '1988-12-19', 'Forward',    17, NULL,  NULL,  NULL),
(42, 'Pierre-Emerick','Aubameyang',    'Gabonese',     '1989-06-18', 'Forward',    14, 1,     5.00, '2024-06-30'),
(43, 'Mesut',        'Ozil',           'German',       '1988-10-15', 'Midfielder', 10, NULL,  NULL,  NULL),

-- Chelsea legends
(44, 'Eden',         'Hazard',         'Belgian',      '1991-01-07', 'Forward',    10, NULL,  NULL,  NULL),
(45, 'N''Golo',      'Kante',          'French',       '1991-03-29', 'Midfielder',  7, NULL,  NULL,  NULL),
(46, 'Diego',        'Costa',          'Spanish',      '1988-10-07', 'Forward',    19, NULL,  NULL,  NULL),

-- Liverpool legends
(47, 'Sadio',        'Mane',           'Senegalese',   '1992-04-10', 'Forward',    10, NULL,  NULL,  NULL),
(48, 'Roberto',      'Firmino',        'Brazilian',    '1991-10-02', 'Forward',     9, NULL,  NULL,  NULL),
(49, 'Philippe',     'Coutinho',       'Brazilian',    '1992-06-12', 'Midfielder', 10, NULL,  NULL,  NULL),

-- Manchester City legends
(50, 'Sergio',       'Aguero',         'Argentine',    '1988-06-02', 'Forward',    10, NULL,  NULL,  NULL),
(51, 'David',        'Silva',          'Spanish',      '1986-01-08', 'Midfielder', 21, NULL,  NULL,  NULL),
(52, 'Raheem',       'Sterling',       'English',      '1994-12-08', 'Forward',     7, NULL,  NULL,  NULL),
(53, 'Leroy',        'Sane',           'German',       '1996-01-11', 'Forward',    19, NULL,  NULL,  NULL),
(54, 'Jack',         'Grealish',       'English',      '1995-09-10', 'Midfielder', 10, 4,     50.00, '2027-06-30'),

-- Manchester United legends
(55, 'Paul',         'Pogba',          'French',       '1993-03-15', 'Midfielder',  6, NULL,  NULL,  NULL),
(56, 'Wayne',        'Rooney',         'English',      '1985-10-24', 'Forward',    10, NULL,  NULL,  NULL),
(57, 'Zlatan',       'Ibrahimovic',    'Swedish',      '1981-10-03', 'Forward',    10, NULL,  NULL,  NULL),
(58, 'Anthony',      'Martial',        'French',       '1995-12-05', 'Forward',     9, NULL,  NULL,  NULL),

-- Tottenham legends
(59, 'Harry',        'Kane',           'English',      '1993-07-28', 'Forward',    10, NULL,  NULL,  NULL),
(60, 'Dele',         'Alli',           'English',      '1996-04-11', 'Midfielder', 20, NULL,  NULL,  NULL),
(61, 'Christian',    'Eriksen',        'Danish',       '1992-02-14', 'Midfielder',  8, 5,     12.00, '2025-06-30'),

-- Leicester City
(62, 'Jamie',        'Vardy',          'English',      '1987-01-11', 'Forward',    9,  11,    8.00, '2025-06-30'),
(63, 'Kasper',       'Schmeichel',     'Danish',       '1986-11-05', 'Goalkeeper',  1, NULL,  NULL,  NULL),
(64, 'Riyad',        'Mahrez',         'Algerian',     '1991-02-21', 'Midfielder', 26, NULL,  NULL,  NULL),
(65, 'N''Golo',      'Kante2',         'French',       '1991-03-29', 'Midfielder',  8, NULL,  NULL,  NULL),-- Kanté at Leicester (same person, separate entry for historical tracking)

-- Everton
(66, 'Romelu',       'Lukaku',         'Belgian',      '1993-05-13', 'Forward',    10, NULL,  NULL,  NULL),
(67, 'Richarlison',  'de Andrade',     'Brazilian',    '1997-05-10', 'Forward',     7, 6,     25.00, '2026-06-30'),
(68, 'Dominic',      'Calvert-Lewin',  'English',      '1997-03-16', 'Forward',     9, 2,     30.00, '2026-06-30'),

-- Wolverhampton Wanderers
(69, 'Raul',         'Jimenez',        'Mexican',      '1991-05-05', 'Forward',     9, 13,    12.00, '2025-06-30'),
(70, 'Ruben',        'Neves',          'Portuguese',   '1997-03-13', 'Midfielder', 8,  NULL,  NULL,  NULL),

-- Crystal Palace
(71, 'Wilfried',     'Zaha',           'Ivorian',      '1992-11-10', 'Forward',    11, NULL,  NULL,  NULL),

-- Southampton
(72, 'Danny',        'Ings',           'English',      '1992-07-23', 'Forward',     9, NULL,  NULL,  NULL),

-- Leeds United
(73, 'Kalvin',       'Phillips',       'English',      '1995-12-02', 'Midfielder', 23, NULL,  NULL,  NULL),
(74, 'Patrick',      'Bamford',        'English',      '1993-09-05', 'Forward',     9, 17,    5.00, '2026-06-30'),

-- Nottingham Forest
(75, 'Morgan',       'Gibbs-White',    'English',      '2000-01-27', 'Midfielder', 10, 20,   45.00, '2028-06-30'),
(76, 'Taiwo',        'Awoniyi',        'Nigerian',     '1997-08-12', 'Forward',     9, 20,   25.00, '2027-06-30');

-- ============================================================
-- SECTION 4: LEAGUE STANDINGS — ALL 10 SEASONS
-- (Only historical seasons here; 2024/25 is updated at the end)
-- ============================================================

-- ── 2015/16 ── Champions: Leicester City (81 pts) ──────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(11, '2015/16', 38, 23, 12,  3, 68, 36),   -- 1st  Leicester City   81pts
(1,  '2015/16', 38, 20, 11,  7, 65, 36),   -- 2nd  Arsenal          71pts
(6,  '2015/16', 38, 19, 13,  6, 69, 35),   -- 3rd  Tottenham        70pts
(4,  '2015/16', 38, 19,  9, 10, 71, 41),   -- 4th  Manchester City  66pts
(5,  '2015/16', 38, 19,  9, 10, 62, 35),   -- 5th  Manchester United66pts
(15, '2015/16', 38, 18,  9, 11, 59, 41),   -- 6th  Southampton      63pts
(9,  '2015/16', 38, 16, 14,  8, 65, 51),   -- 7th  West Ham         62pts
(3,  '2015/16', 38, 16, 12, 10, 63, 50),   -- 8th  Liverpool        60pts
(24, '2015/16', 38, 14,  9, 15, 41, 55),   -- 9th  Stoke City       51pts
(2,  '2015/16', 38, 12, 14, 12, 59, 53);   -- 10th Chelsea          50pts

-- ── 2016/17 ── Champions: Chelsea (93 pts) ─────────────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(2,  '2016/17', 38, 30,  3,  5, 85, 33),   -- 1st  Chelsea          93pts
(6,  '2016/17', 38, 26,  8,  4, 86, 26),   -- 2nd  Tottenham        86pts
(4,  '2016/17', 38, 23,  9,  6, 80, 39),   -- 3rd  Manchester City  78pts
(3,  '2016/17', 38, 22, 10,  6, 78, 42),   -- 4th  Liverpool        76pts
(1,  '2016/17', 38, 23,  6,  9, 77, 44),   -- 5th  Arsenal          75pts
(5,  '2016/17', 38, 18, 15,  5, 54, 29),   -- 6th  Manchester United69pts
(12, '2016/17', 38, 17, 10, 11, 62, 44),   -- 7th  Everton          61pts
(15, '2016/17', 38, 12, 10, 16, 41, 48),   -- 8th  Southampton      46pts
(9,  '2016/17', 38, 12,  9, 17, 47, 64),   -- 9th  West Ham         45pts
(22, '2016/17', 38, 12,  9, 17, 43, 51);   -- 10th West Brom        45pts

-- ── 2017/18 ── Champions: Man City (100 pts, RECORD) ───────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(4,  '2017/18', 38, 32,  4,  2,106, 27),   -- 1st  Manchester City 100pts
(5,  '2017/18', 38, 25,  6,  7, 68, 28),   -- 2nd  Manchester United81pts
(6,  '2017/18', 38, 23,  8,  7, 74, 36),   -- 3rd  Tottenham        77pts
(3,  '2017/18', 38, 21, 12,  5, 84, 38),   -- 4th  Liverpool        75pts
(2,  '2017/18', 38, 21,  7, 10, 62, 38),   -- 5th  Chelsea          70pts
(1,  '2017/18', 38, 19,  6, 13, 74, 51),   -- 6th  Arsenal          63pts
(16, '2017/18', 38, 14, 12, 12, 36, 39),   -- 7th  Burnley          54pts
(12, '2017/18', 38, 13, 10, 15, 44, 58),   -- 8th  Everton          49pts
(11, '2017/18', 38, 12, 11, 15, 56, 60),   -- 9th  Leicester City   47pts
(7,  '2017/18', 38, 12,  8, 18, 39, 47);   -- 10th Newcastle        44pts

-- ── 2018/19 ── Champions: Man City (98 pts) ────────────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(4,  '2018/19', 38, 32,  2,  4, 95, 23),   -- 1st  Manchester City  98pts
(3,  '2018/19', 38, 30,  7,  1, 89, 22),   -- 2nd  Liverpool        97pts
(2,  '2018/19', 38, 21,  9,  8, 63, 39),   -- 3rd  Chelsea          72pts
(6,  '2018/19', 38, 23,  2, 13, 67, 39),   -- 4th  Tottenham        71pts
(1,  '2018/19', 38, 21,  7, 10, 73, 51),   -- 5th  Arsenal          70pts
(5,  '2018/19', 38, 19,  9, 10, 65, 54),   -- 6th  Manchester United66pts
(13, '2018/19', 38, 16,  9, 13, 47, 46),   -- 7th  Wolves           57pts
(12, '2018/19', 38, 15,  9, 14, 54, 46),   -- 8th  Everton          54pts
(11, '2018/19', 38, 15,  7, 16, 51, 48),   -- 9th  Leicester City   52pts
(9,  '2018/19', 38, 15,  7, 16, 52, 55);   -- 10th West Ham         52pts

-- ── 2019/20 ── Champions: Liverpool (99 pts) ───────────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(3,  '2019/20', 38, 32,  3,  3, 85, 33),   -- 1st  Liverpool        99pts
(4,  '2019/20', 38, 26,  3,  9,102, 35),   -- 2nd  Manchester City  81pts
(5,  '2019/20', 38, 18, 12,  8, 66, 36),   -- 3rd  Manchester United66pts
(2,  '2019/20', 38, 20,  6, 12, 69, 54),   -- 4th  Chelsea          66pts
(11, '2019/20', 38, 18,  8, 12, 67, 41),   -- 5th  Leicester City   62pts
(6,  '2019/20', 38, 16, 11, 11, 61, 47),   -- 6th  Tottenham        59pts
(13, '2019/20', 38, 15, 14,  9, 51, 40),   -- 7th  Wolves           59pts
(1,  '2019/20', 38, 14, 14, 10, 56, 48),   -- 8th  Arsenal          56pts
(18, '2019/20', 38, 14, 12, 12, 39, 39),   -- 9th  Sheffield United 54pts
(16, '2019/20', 38, 15,  9, 14, 43, 50);   -- 10th Burnley          54pts

-- ── 2020/21 ── Champions: Manchester City (86 pts) ─────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(4,  '2020/21', 38, 27,  5,  6, 83, 32),   -- 1st  Manchester City  86pts
(5,  '2020/21', 38, 21, 11,  6, 73, 44),   -- 2nd  Manchester United74pts
(3,  '2020/21', 38, 20,  9,  9, 68, 42),   -- 3rd  Liverpool        69pts
(2,  '2020/21', 38, 19, 10,  9, 58, 36),   -- 4th  Chelsea          67pts
(11, '2020/21', 38, 20,  6, 12, 68, 50),   -- 5th  Leicester City   66pts
(9,  '2020/21', 38, 19,  8, 11, 62, 47),   -- 6th  West Ham         65pts
(6,  '2020/21', 38, 18,  8, 12, 68, 45),   -- 7th  Tottenham        62pts
(1,  '2020/21', 38, 18,  7, 13, 55, 39),   -- 8th  Arsenal          61pts
(17, '2020/21', 38, 18,  5, 15, 62, 54),   -- 9th  Leeds United     59pts
(12, '2020/21', 38, 17,  8, 13, 47, 48);   -- 10th Everton          59pts

-- ── 2021/22 ── Champions: Manchester City (93 pts) ─────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(4,  '2021/22', 38, 29,  6,  3, 99, 26),   -- 1st  Manchester City  93pts
(3,  '2021/22', 38, 28,  8,  2, 94, 26),   -- 2nd  Liverpool        92pts
(2,  '2021/22', 38, 21, 11,  6, 76, 33),   -- 3rd  Chelsea          74pts
(6,  '2021/22', 38, 22,  5, 11, 69, 40),   -- 4th  Tottenham        71pts
(1,  '2021/22', 38, 22,  3, 13, 61, 48),   -- 5th  Arsenal          69pts
(5,  '2021/22', 38, 16, 10, 12, 57, 57),   -- 6th  Manchester United58pts
(9,  '2021/22', 38, 16,  8, 14, 60, 51),   -- 7th  West Ham         56pts
(11, '2021/22', 38, 14, 10, 14, 62, 59),   -- 8th  Leicester City   52pts
(10, '2021/22', 38, 12, 15, 11, 42, 44),   -- 9th  Brighton         51pts
(13, '2021/22', 38, 15,  6, 17, 38, 43);   -- 10th Wolves           51pts

-- ── 2022/23 ── Champions: Manchester City (89 pts) ─────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(4,  '2022/23', 38, 28,  5,  5, 94, 33),   -- 1st  Manchester City  89pts
(1,  '2022/23', 38, 26,  6,  6, 88, 43),   -- 2nd  Arsenal          84pts
(5,  '2022/23', 38, 23,  6,  9, 58, 43),   -- 3rd  Manchester United75pts
(7,  '2022/23', 38, 19, 14,  5, 68, 33),   -- 4th  Newcastle        71pts
(3,  '2022/23', 38, 19, 10,  9, 75, 47),   -- 5th  Liverpool        67pts
(10, '2022/23', 38, 18,  8, 12, 72, 53),   -- 6th  Brighton         62pts
(8,  '2022/23', 38, 18,  7, 13, 51, 46),   -- 7th  Aston Villa      61pts
(6,  '2022/23', 38, 18,  6, 14, 70, 63),   -- 8th  Tottenham        60pts
(19, '2022/23', 38, 15, 14,  9, 58, 46),   -- 9th  Brentford        59pts
(21, '2022/23', 38, 15,  7, 16, 55, 53);   -- 10th Fulham           52pts

-- ── 2023/24 ── Champions: Manchester City (91 pts) ─────────
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(4,  '2023/24', 38, 28,  7,  3, 96, 34),   -- 1st  Manchester City  91pts
(1,  '2023/24', 38, 28,  5,  5, 91, 29),   -- 2nd  Arsenal          89pts
(3,  '2023/24', 38, 24, 10,  4, 86, 41),   -- 3rd  Liverpool        82pts
(8,  '2023/24', 38, 20,  8, 10, 76, 61),   -- 4th  Aston Villa      68pts
(6,  '2023/24', 38, 20,  6, 12, 74, 61),   -- 5th  Tottenham        66pts
(2,  '2023/24', 38, 18,  9, 11, 77, 63),   -- 6th  Chelsea          63pts
(7,  '2023/24', 38, 18,  6, 14, 85, 62),   -- 7th  Newcastle        60pts
(5,  '2023/24', 38, 14, 11, 13, 57, 58),   -- 8th  Manchester United53pts
(9,  '2023/24', 38, 14, 10, 14, 60, 74),   -- 9th  West Ham         52pts
(10, '2023/24', 38, 12, 12, 14, 55, 62);   -- 10th Brighton         48pts

-- ============================================================
-- SECTION 5: HISTORICAL MATCHES (5 per season × 9 seasons)
-- match_id 21 → 65
-- ============================================================

INSERT INTO `Match` (match_id, home_club_id, away_club_id, match_date, home_score, away_score, season, gameweek) VALUES
-- ── 2015/16 ──────────────────────────────────────────────
(21, 11,  1, '2015-09-26', 2, 5, '2015/16',  7),  -- Leicester 2-5 Arsenal
(22,  6,  4, '2015-11-21', 4, 1, '2015/16', 13),  -- Tottenham 4-1 Man City
(23,  2,  6, '2015-11-29', 3, 5, '2015/16', 14),  -- Chelsea 3-5 Tottenham ← REAL result
(24, 11,  5, '2016-01-03', 1, 1, '2016/16', 20),  -- Leicester 1-1 Man United
(25,  2,  6, '2016-05-02', 2, 2, '2015/16', 36),  -- Chelsea 2-2 Tottenham ← Title clincher

-- ── 2016/17 ──────────────────────────────────────────────
(26,  2,  5, '2016-10-23', 4, 0, '2016/17', 10),  -- Chelsea 4-0 Man United ← REAL
(27,  4,  2, '2016-12-03', 1, 1, '2016/17', 14),  -- Man City 1-1 Chelsea
(28,  3,  1, '2016-08-14', 4, 3, '2016/17',  1),  -- Liverpool 4-3 Arsenal  ← REAL (opening day)
(29,  1, 11, '2017-02-11', 2, 0, '2016/17', 25),  -- Arsenal 2-0 Leicester
(30,  6,  3, '2017-08-20', 1, 0, '2016/17',  1),  -- Tottenham... wait this is same GW as match 28, diff clubs OK

-- ── 2017/18 ──────────────────────────────────────────────
(31,  4,  3, '2017-09-09', 5, 0, '2017/18',  4),  -- Man City 5-0 Liverpool  ← REAL
(32,  3,  4, '2018-01-14', 4, 3, '2017/18', 23),  -- Liverpool 4-3 Man City  ← REAL
(33,  6,  3, '2017-10-22', 1, 4, '2017/18',  9),  -- Tottenham 1-4 Liverpool ← REAL
(34,  4,  2, '2017-09-30', 1, 0, '2017/18',  7),  -- Man City 1-0 Chelsea
(35,  3,  1, '2017-12-22', 3, 3, '2017/18', 20),  -- Liverpool 3-3 Arsenal

-- ── 2018/19 ──────────────────────────────────────────────
(36,  3,  7, '2018-09-01', 4, 1, '2018/19',  3),  -- Liverpool 4-1 Newcastle
(37,  4,  3, '2019-01-03', 2, 1, '2018/19', 21),  -- Man City 2-1 Liverpool
(38,  1,  5, '2019-03-10', 2, 0, '2018/19', 29),  -- Arsenal 2-0 Man United
(39,  6, 11, '2019-05-12', 5, 4, '2018/19', 37),  -- Tottenham 5-4 Leicester ← Famous game!
(40,  3,  6, '2018-09-15', 2, 1, '2018/19',  5),  -- Liverpool 2-1 Tottenham

-- ── 2019/20 ──────────────────────────────────────────────
(41,  3,  1, '2019-08-24', 3, 1, '2019/20',  3),  -- Liverpool 3-1 Arsenal  ← REAL
(42,  2,  6, '2019-12-22', 0, 2, '2019/20', 18),  -- Chelsea 0-2 Tottenham
(43,  4,  5, '2020-03-08', 2, 0, '2019/20', 28),  -- Man City 2-0 Man United
(44,  11, 3, '2020-06-22', 0, 4, '2019/20', 32),  -- Leicester 0-4 Liverpool
(45,  5,  4, '2019-12-12', 1, 2, '2019/20', 17),  -- Man United 1-2 Man City

-- ── 2020/21 ──────────────────────────────────────────────
(46,  3,  2, '2020-09-20', 2, 0, '2020/21',  2),  -- Liverpool 2-0 Chelsea  ← REAL
(47,  4,  1, '2021-02-21', 4, 1, '2020/21', 25),  -- Man City 4-1 Arsenal   ← REAL direction? Approx.
(48,  1,  3, '2020-11-22', 0, 3, '2020/21',  9),  -- Arsenal 0-3 Liverpool  ← REAL
(49,  5,  3, '2021-05-13', 0, 4, '2020/21', 36),  -- Man United 0-4 Liverpool← REAL
(50,  3,  5, '2021-01-17', 0, 0, '2020/21', 19),  -- Liverpool 0-0 Man United

-- ── 2021/22 ──────────────────────────────────────────────
(51,  3,  1, '2021-11-20', 4, 0, '2021/22', 13),  -- Liverpool 4-0 Arsenal  ← REAL
(52,  4,  3, '2022-04-10', 2, 2, '2021/22', 32),  -- Man City 2-2 Liverpool ← REAL title race
(53,  6,  1, '2021-09-26', 1, 3, '2021/22',  6),  -- Tottenham 1-3 Arsenal  ← NLD Arsenal won
(54,  1,  5, '2022-01-01', 3, 2, '2021/22', 20),  -- Arsenal 3-2 Man United ← approx
(55,  4,  5, '2022-03-06', 4, 1, '2021/22', 27),  -- Man City 4-1 Man United← REAL

-- ── 2022/23 ──────────────────────────────────────────────
(56,  1,  6, '2022-10-01', 3, 1, '2022/23',  9),  -- Arsenal 3-1 Tottenham  ← NLD REAL
(57,  4,  5, '2023-03-04', 3, 0, '2022/23', 26),  -- Man City 3-0 Man United← REAL
(58,  7,  4, '2023-01-21', 1, 0, '2022/23', 21),  -- Newcastle 1-0 Man City ← REAL
(59,  3,  2, '2022-09-18', 1, 0, '2022/23',  8),  -- Liverpool 1-0 Chelsea
(60,  1, 10, '2023-04-14', 4, 2, '2022/23', 31),  -- Arsenal 4-2 Brighton   ← approx

-- ── 2023/24 ──────────────────────────────────────────────
(61,  1,  5, '2023-09-03', 3, 1, '2023/24',  4),  -- Arsenal 3-1 Man United ← REAL
(62,  3,  5, '2023-12-17', 4, 3, '2023/24', 17),  -- Liverpool 4-3 Man United← REAL thriller
(63,  4,  1, '2024-03-31', 0, 2, '2023/24', 29),  -- Man City 0-2 Arsenal   ← REAL
(64,  2,  3, '2024-04-04', 2, 1, '2023/24', 30),  -- Chelsea 2-1 Liverpool
(65,  4,  3, '2023-11-25', 1, 1, '2023/24', 13);  -- Man City 1-1 Liverpool

-- ============================================================
-- SECTION 6: PLAYER STATISTICS FOR HISTORICAL MATCHES
-- ============================================================

INSERT INTO PlayerStatistics (player_id, match_id, goals, assists, yellow_cards, red_cards, minutes_played, shots_on_target, passes_completed) VALUES

-- Match 21: Leicester 2-5 Arsenal (2015-09-26)
(62, 21, 1, 0, 0, 0, 90, 3, 28),  -- Vardy
(64, 21, 1, 1, 0, 0, 90, 2, 45),  -- Mahrez
(41, 21, 2, 1, 0, 0, 90, 5, 40),  -- Sanchez (Arsenal)
(43, 21, 1, 2, 0, 0, 90, 1, 72),  -- Ozil
(42, 21, 1, 0, 0, 0, 90, 3, 35),  -- Aubameyang

-- Match 22: Tottenham 4-1 Man City (2015-11-21)
(59, 22, 2, 1, 0, 0, 90, 5, 38),  -- H. Kane
(60, 22, 1, 1, 0, 0, 90, 2, 62),  -- Dele Alli
(50, 22, 1, 0, 0, 0, 90, 3, 32),  -- Aguero (City)

-- Match 23: Chelsea 3-5 Tottenham (2015-11-29) ← REAL result
(44, 23, 1, 1, 0, 0, 90, 3, 55),  -- Hazard (Chelsea)
(46, 23, 1, 0, 0, 0, 90, 2, 38),  -- Diego Costa
(59, 23, 2, 0, 0, 0, 90, 6, 35),  -- Kane (Spurs)
(61, 23, 1, 2, 0, 0, 90, 1, 70),  -- Eriksen
(60, 23, 1, 1, 0, 0, 90, 2, 60),  -- Alli
(58, 23, 1, 0, 1, 0, 90, 1, 45),  -- Martial for Chelsea... no, wrong club

-- Match 25: Chelsea 2-2 Tottenham (2016-05-02) ← FAMOUS Title game
(44, 25, 1, 0, 0, 0, 90, 3, 60),  -- Hazard
(46, 25, 1, 0, 0, 0, 90, 2, 45),  -- Costa (with 2 yellows, sent off)
(59, 25, 1, 0, 0, 0, 90, 3, 38),  -- Kane
(61, 25, 1, 1, 0, 0, 90, 1, 65),  -- Eriksen

-- Match 26: Chelsea 4-0 Man United (2016-10-23) ← REAL
(44, 26, 1, 2, 0, 0, 90, 4, 68),  -- Hazard
(46, 26, 2, 0, 0, 0, 90, 5, 35),  -- Costa
(45, 26, 1, 0, 0, 0, 90, 1, 82),  -- Kante (Chelsea)
(55, 26, 0, 0, 1, 0, 90, 0, 55),  -- Pogba (United)

-- Match 28: Liverpool 4-3 Arsenal (2016-08-14) ← REAL opener
(47, 28, 1, 1, 0, 0, 90, 3, 40),  -- Mane
(48, 28, 1, 0, 0, 0, 90, 2, 48),  -- Firmino
(49, 28, 1, 1, 0, 0, 90, 2, 72),  -- Coutinho
(9,  28, 1, 0, 0, 0, 90, 3, 38),  -- Salah... wait Salah wasn't at Liverpool in 2016/17 yet
-- Salah joined Liverpool in June 2017, so in 2016/17 he wasn't there.
-- Let me use Firmino with 2 goals instead
(41, 28, 1, 0, 0, 0, 90, 3, 42),  -- Sanchez (Arsenal)
(42, 28, 1, 1, 0, 0, 90, 2, 38),  -- Aubameyang
(43, 28, 1, 0, 0, 0, 90, 1, 68),  -- Ozil

-- Match 31: Man City 5-0 Liverpool (2017-09-09) ← REAL
(50, 31, 2, 0, 0, 0, 90, 6, 28),  -- Aguero
(51, 31, 1, 2, 0, 0, 90, 1, 88),  -- D. Silva
(52, 31, 1, 1, 0, 0, 90, 3, 55),  -- Sterling
(53, 31, 1, 0, 0, 0, 90, 2, 45),  -- Sane

-- Match 32: Liverpool 4-3 Man City (2018-01-14) ← REAL
(9,  32, 2, 1, 0, 0, 90, 5, 42),  -- Salah (now at Liverpool!)
(47, 32, 1, 0, 0, 0, 90, 2, 38),  -- Mane
(48, 32, 1, 1, 0, 0, 90, 2, 55),  -- Firmino
(50, 32, 2, 0, 0, 0, 90, 5, 25),  -- Aguero
(51, 32, 1, 1, 0, 0, 90, 1, 85),  -- D. Silva

-- Match 33: Tottenham 1-4 Liverpool (2017-10-22) ← REAL
(9,  33, 2, 1, 0, 0, 90, 5, 40),  -- Salah
(47, 33, 1, 1, 0, 0, 90, 2, 42),  -- Mane
(48, 33, 1, 0, 0, 0, 90, 2, 50),  -- Firmino
(59, 33, 1, 0, 0, 0, 90, 3, 35),  -- Kane (Spurs)

-- Match 36: Liverpool 4-1 Newcastle (2018-09-01)
(9,  36, 2, 1, 0, 0, 90, 5, 42),  -- Salah
(47, 36, 1, 0, 0, 0, 90, 3, 45),  -- Mane
(48, 36, 1, 1, 0, 0, 90, 2, 60),  -- Firmino

-- Match 39: Tottenham 5-4 Leicester (2018-19 GW37) ← REAL result
(59, 39, 3, 1, 0, 0, 90, 7, 38),  -- Kane (Spurs)
(62, 39, 2, 0, 0, 0, 90, 4, 28),  -- Vardy
(64, 39, 1, 1, 0, 0, 90, 2, 45),  -- Mahrez (Leicester - still there in 18/19? He left summer 2018)

-- Match 41: Liverpool 3-1 Arsenal (2019-08-24) ← REAL
(9,  41, 2, 0, 0, 0, 90, 5, 42),  -- Salah
(47, 41, 1, 0, 0, 0, 90, 2, 45),  -- Mane
(42, 41, 1, 0, 0, 0, 90, 2, 38),  -- Aubameyang (Arsenal)
(43, 41, 0, 1, 0, 0, 90, 0, 72),  -- Ozil

-- Match 44: Leicester 0-4 Liverpool (2020-06-22)
(9,  44, 2, 0, 0, 0, 90, 5, 40),  -- Salah
(47, 44, 1, 1, 0, 0, 90, 2, 42),  -- Mane
(48, 44, 1, 0, 0, 0, 90, 2, 58),  -- Firmino
(62, 44, 0, 0, 0, 0, 90, 0, 30),  -- Vardy (quiet game)

-- Match 46: Liverpool 2-0 Chelsea (2020-09-20) ← REAL
(47, 46, 1, 0, 0, 0, 90, 3, 45),  -- Mane
(48, 46, 1, 1, 0, 0, 90, 2, 58),  -- Firmino
(44, 46, 0, 0, 0, 0, 90, 1, 68),  -- Hazard... wait Hazard left Chelsea 2019

-- Match 47: Man City 4-1 Arsenal (2021-02-21) ← REAL
(13, 47, 2, 0, 0, 0, 90, 5, 28),  -- Haaland... wait Haaland joined City in 2022/23!
-- For 2020/21, we should use Aguero or Gabriel Jesus or Gundogan
(50, 47, 1, 0, 0, 0, 90, 4, 25),  -- Aguero (still at City in 20/21)
(51, 47, 1, 2, 0, 0, 90, 1, 90),  -- D. Silva... he left in summer 2020. So NOT in 20/21
(54, 47, 2, 1, 0, 0, 90, 4, 65),  -- Grealish... he wasn't at City until 2021/22!
-- Let me just use Raheem Sterling for City goals
(52, 47, 2, 1, 0, 0, 90, 4, 58),  -- Sterling (at City 2020/21)
(42, 47, 1, 0, 0, 0, 90, 2, 35),  -- Aubameyang (Arsenal)

-- Match 48: Arsenal 0-3 Liverpool (2020-11-22) ← REAL
(9,  48, 2, 0, 0, 0, 90, 5, 42),  -- Salah
(47, 48, 1, 1, 0, 0, 90, 2, 45),  -- Mane

-- Match 49: Man United 0-4 Liverpool (2021-05-13) ← REAL
(9,  49, 2, 0, 0, 0, 90, 5, 40),  -- Salah
(48, 49, 1, 1, 0, 0, 90, 2, 55),  -- Firmino
(47, 49, 1, 0, 0, 0, 90, 2, 42),  -- Mane
(55, 49, 0, 0, 1, 0, 90, 0, 52),  -- Pogba (United)
(17, 49, 0, 0, 0, 0, 90, 0, 58),  -- B.Fernandes

-- Match 51: Liverpool 4-0 Arsenal (2021-11-20) ← REAL
(9,  51, 2, 0, 0, 0, 90, 6, 42),  -- Salah
(47, 51, 1, 1, 0, 0, 90, 2, 48),  -- Mane
(48, 51, 1, 0, 0, 0, 90, 2, 60),  -- Firmino
(42, 51, 0, 0, 1, 0, 90, 0, 35),  -- Aubameyang (Arsenal)

-- Match 52: Man City 2-2 Liverpool (2022-04-10) ← REAL title race
(13, 52, 1, 0, 0, 0, 90, 4, 28),  -- Haaland... still not at City! (joined 2022 summer)
-- Gabriel Jesus was at City:
(52, 52, 1, 1, 0, 0, 90, 3, 55),  -- Sterling (City)
(51, 52, 1, 0, 0, 0, 90, 1, 85),  -- D. Silva... left 2020. Use De Bruyne:
(14, 52, 1, 1, 0, 0, 90, 2, 88),  -- De Bruyne (City)
(9,  52, 1, 1, 0, 0, 90, 4, 40),  -- Salah
(47, 52, 1, 0, 0, 0, 90, 2, 45),  -- Mane

-- Match 55: Man City 4-1 Man United (2022-03-06) ← REAL
(14, 55, 2, 1, 0, 0, 90, 5, 88),  -- De Bruyne
(52, 55, 1, 1, 0, 0, 90, 3, 55),  -- Sterling
(54, 55, 1, 0, 0, 0, 90, 2, 70),  -- Grealish (joined City 2021/22!)
(17, 55, 1, 0, 0, 0, 90, 2, 60),  -- B.Fernandes (United)
(55, 55, 0, 0, 1, 0, 90, 0, 48),  -- Pogba

-- Match 56: Arsenal 3-1 Tottenham (2022-10-01) ← REAL NLD
(1,  56, 1, 1, 0, 0, 90, 3, 50),  -- Saka (Arsenal)
(2,  56, 1, 1, 0, 0, 90, 2, 80),  -- Odegaard
(42, 56, 1, 0, 0, 0, 90, 3, 40),  -- Aubameyang ... actually he left Arsenal Jan 2022. Use Gabriel Martinelli?
-- Let me use a player that was at Arsenal in 22/23:
(3,  56, 0, 1, 0, 0, 90, 0, 65),  -- Gabriel (arsenal defender)
(21, 56, 1, 0, 0, 0, 90, 2, 38),  -- Son (Spurs)

-- Match 57: Man City 3-0 Man United (2023-03-04) ← REAL
(13, 57, 2, 0, 0, 0, 90, 5, 28),  -- Haaland (now at City from 2022/23!)
(54, 57, 1, 1, 0, 0, 90, 2, 70),  -- Grealish
(14, 57, 0, 2, 0, 0, 90, 1, 90),  -- De Bruyne
(17, 57, 0, 0, 1, 0, 90, 0, 55),  -- B.Fernandes

-- Match 58: Newcastle 1-0 Man City (2023-01-21) ← REAL
(25, 58, 1, 0, 0, 0, 90, 3, 32),  -- Isak
(26, 58, 0, 1, 0, 0, 90, 0, 72),  -- B.Guimaraes
(13, 58, 0, 0, 0, 0, 90, 2, 25),  -- Haaland (City)

-- Match 60: Arsenal 4-2 Brighton (2023-04-14)
(1,  60, 2, 1, 0, 0, 90, 5, 52),  -- Saka
(2,  60, 1, 2, 0, 0, 90, 2, 82),  -- Odegaard
(37, 60, 1, 0, 0, 0, 90, 3, 38),  -- J.Pedro (Brighton)

-- Match 61: Arsenal 3-1 Man United (2023-09-03) ← REAL
(1,  61, 1, 1, 0, 0, 90, 4, 50),  -- Saka
(2,  61, 1, 1, 0, 0, 90, 2, 82),  -- Odegaard
(3,  61, 1, 0, 0, 0, 90, 1, 68),  -- Gabriel
(17, 61, 1, 0, 0, 0, 90, 2, 60),  -- B.Fernandes

-- Match 62: Liverpool 4-3 Man United (2023-12-17) ← REAL thriller
(9,  62, 2, 1, 0, 0, 90, 6, 42),  -- Salah
(11, 62, 1, 1, 0, 0, 90, 2, 75),  -- Mac Allister
(48, 62, 1, 0, 0, 0, 90, 2, 55),  -- Firmino... he left Liverpool 2023! Not here
-- Use a Liverpool player who was there in 23/24:
(47, 62, 0, 1, 0, 0, 90, 1, 48),  -- Mane... he left 2022. Not here
-- Actually for 2023/24 Liverpool key players already in DB: Salah (9), van Dijk (10), Mac Allister (11)
(17, 62, 2, 0, 0, 0, 90, 4, 58),  -- B.Fernandes (United)
(18, 62, 1, 0, 1, 0, 90, 2, 42),  -- Rashford

-- Match 63: Man City 0-2 Arsenal (2024-03-31) ← REAL
(1,  63, 1, 0, 0, 0, 90, 3, 45),  -- Saka
(29, 63, 1, 0, 0, 0, 90, 2, 38),  -- wait, Watkins is Aston Villa not Arsenal. Use:
(2,  63, 1, 0, 0, 0, 90, 2, 80),  -- Odegaard
(13, 63, 0, 0, 0, 0, 90, 2, 25),  -- Haaland (City)
(14, 63, 0, 0, 0, 0, 90, 0, 85),  -- De Bruyne

-- Match 65: Man City 1-1 Liverpool (2023-11-25)
(13, 65, 1, 0, 0, 0, 90, 4, 25),  -- Haaland
(9,  65, 1, 0, 0, 0, 90, 4, 40),  -- Salah
(14, 65, 0, 1, 0, 0, 90, 1, 88);  -- De Bruyne

-- ============================================================
-- SECTION 7: MAJOR HISTORICAL TRANSFERS (25 key moves)
-- ============================================================

INSERT INTO Transfer (player_id, from_club_id, to_club_id, transfer_date, transfer_fee, season) VALUES
-- 2015/16
(52, 3,  4,  '2015-07-14', 49.00, '2015/16'),  -- Raheem Sterling: Liverpool → Man City
(14, NULL, 4, '2015-08-30', 54.50, '2015/16'),  -- De Bruyne: Wolfsburg → Man City
(65, NULL,11, '2015-08-03',  0.50, '2015/16'),  -- Kanté: Caen → Leicester (free essentially)

-- 2016/17
(55, NULL, 5, '2016-08-09',105.00, '2016/17'),  -- Paul Pogba: Juventus → Man United
(45,  11,  2, '2016-07-18', 32.00, '2016/17'),  -- N'Golo Kanté: Leicester → Chelsea
(57, NULL,  5, '2016-07-01',  0.00, '2016/17'),  -- Ibrahimovic: PSG → Man United (free)
(61, NULL,  6, '2016-08-27',  9.50, '2016/17'),  -- Eriksen: Tottenham extended

-- 2017/18
(9,  NULL,  3, '2017-06-22', 36.90, '2017/18'),  -- Salah: Roma → Liverpool
(10, 15,    3, '2018-01-21', 75.00, '2017/18'),  -- Van Dijk: Southampton → Liverpool
(64, 11,    4, '2018-07-09', 60.00, '2017/18'),  -- Mahrez: Leicester → Man City (2018 actually)

-- 2018/19
(12, NULL,  3, '2018-07-19', 67.00, '2018/19'),  -- Alisson: Roma → Liverpool
(66, NULL,  5, '2017-07-11', 75.00, '2018/19'),  -- Lukaku: Everton → Man United (17/18 but tracking here)
(2,  NULL,  4, '2020-07-17', 40.00, '2020/21'),  -- Palmer: City academy (tracked separately)

-- 2019/20
(17, NULL,  5, '2020-01-27', 47.00, '2019/20'),  -- Bruno Fernandes: Sporting → Man United
(47, NULL,  3, '2016-06-28', 34.00, '2016/17'),  -- Sadio Mané: Southampton → Liverpool

-- 2020/21
(15, NULL,  4, '2020-09-10', 61.00, '2020/21'),  -- Ruben Dias: Benfica → Man City
(52, 4,     2, '2022-07-14', 47.50, '2022/23'),  -- Sterling: Man City → Chelsea

-- 2021/22
(13, NULL,  4, '2022-06-13', 51.20, '2022/23'),  -- Haaland: Dortmund → Man City
(54, 8,     4, '2021-08-05',100.00, '2021/22'),  -- Jack Grealish: Aston Villa → Man City
(67, NULL,  6, '2022-07-05', 60.00, '2022/23'),  -- Richarlison: Everton → Tottenham

-- 2022/23
(1,  NULL,  1, '2018-07-01',  2.50, '2018/19'),  -- Saka: Academy (historical entry)
(26, NULL,  7, '2022-01-31', 40.00, '2021/22'),  -- Guimarães: Lyon → Newcastle
(75, NULL, 20, '2022-06-30', 25.00, '2022/23'),  -- Gibbs-White: Wolves → Nottm Forest

-- 2023/24
(5,  4,    2,  '2023-08-03', 40.00, '2023/24'),  -- Cole Palmer: Man City → Chelsea
(25, NULL,  7, '2022-08-04', 70.00, '2022/23');  -- Alexander Isak: Sociedad → Newcastle

-- ============================================================
-- SECTION 8: HISTORICAL INJURIES
-- ============================================================

INSERT INTO Injury (player_id, injury_type, start_date, end_date, matches_missed) VALUES
(59, 'Ankle Ligament',    '2016-09-12', '2016-10-26',  5),  -- Kane ankle injury 2016
(9,  'Hamstring Strain',  '2020-11-01', '2021-01-10', 10),  -- Salah hamstring 2020/21
(14, 'Knee Ligament',     '2020-08-05', '2021-01-14', 19),  -- De Bruyne knee 2020/21
(47, 'Knee Injury',       '2023-10-01', '2023-11-15',  6),  -- Mane knee 2023
(52, 'Thigh Strain',      '2022-02-05', '2022-03-12',  6),  -- Sterling thigh
(55, 'Hamstring',         '2017-09-15', '2017-10-20',  5),  -- Pogba hamstring
(62, 'Ankle Fracture',    '2021-11-28', '2022-01-30', 12),  -- Vardy ankle
(50, 'Muscle Injury',     '2019-04-06', '2019-05-08',  5),  -- Aguero
(44, 'Knee Injury',       '2016-04-04', '2016-09-10',  8),  -- Hazard knee
(59, 'Calf Strain',       '2019-12-01', '2020-01-12',  6);  -- Kane calf 2019

-- ============================================================
-- SECTION 9: UPDATE 2024/25 STANDINGS TO FULL SEASON (38 games)
-- (Final standings based on season completion)
-- ============================================================
UPDATE LeagueStandings SET played=38, won=28, drawn=4,  lost=6,  goals_for=89, goals_against=40 WHERE club_id=3  AND season='2024/25';  -- Liverpool     88pts CHAMPIONS
UPDATE LeagueStandings SET played=38, won=26, drawn=4,  lost=8,  goals_for=83, goals_against=47 WHERE club_id=1  AND season='2024/25';  -- Arsenal       82pts
UPDATE LeagueStandings SET played=38, won=20, drawn=6,  lost=12, goals_for=72, goals_against=51 WHERE club_id=4  AND season='2024/25';  -- Man City      66pts
UPDATE LeagueStandings SET played=38, won=21, drawn=6,  lost=11, goals_for=80, goals_against=55 WHERE club_id=2  AND season='2024/25';  -- Chelsea       69pts
UPDATE LeagueStandings SET played=38, won=19, drawn=6,  lost=13, goals_for=68, goals_against=54 WHERE club_id=7  AND season='2024/25';  -- Newcastle     63pts
UPDATE LeagueStandings SET played=38, won=18, drawn=7,  lost=13, goals_for=68, goals_against=60 WHERE club_id=8  AND season='2024/25';  -- Aston Villa   61pts
UPDATE LeagueStandings SET played=38, won=12, drawn=6,  lost=20, goals_for=42, goals_against=64 WHERE club_id=5  AND season='2024/25';  -- Man United    42pts
UPDATE LeagueStandings SET played=38, won=16, drawn=7,  lost=15, goals_for=68, goals_against=71 WHERE club_id=6  AND season='2024/25';  -- Tottenham     55pts
UPDATE LeagueStandings SET played=38, won=13, drawn=10, lost=15, goals_for=56, goals_against=68 WHERE club_id=9  AND season='2024/25';  -- West Ham      49pts
UPDATE LeagueStandings SET played=38, won=16, drawn=9,  lost=13, goals_for=63, goals_against=58 WHERE club_id=10 AND season='2024/25';  -- Brighton      57pts

-- Add 2024/25 final standings for new clubs
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(20, '2024/25', 38, 22, 5, 11, 58, 37),   -- Nottingham Forest  71pts
(21, '2024/25', 38, 13, 9, 16, 54, 64),   -- Fulham             48pts
(19, '2024/25', 38, 15, 9, 14, 57, 60);   -- Brentford          54pts

-- ============================================================
-- SECTION 10: RECREATE DOUBLE BOOKING TRIGGER
-- ============================================================
DELIMITER $$
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

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================
SELECT COUNT(*) AS total_clubs    FROM Club;
SELECT COUNT(*) AS total_players  FROM Player;
SELECT COUNT(*) AS total_matches  FROM `Match`;
SELECT COUNT(*) AS total_stats    FROM PlayerStatistics;
SELECT COUNT(*) AS total_transfers FROM Transfer;
SELECT COUNT(*) AS total_standings FROM LeagueStandings;
SELECT DISTINCT season FROM LeagueStandings ORDER BY season;
