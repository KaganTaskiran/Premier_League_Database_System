-- ============================================================
-- Premier League Data Management System - Sample Data
-- SE 2230: Database Systems - Term Project
-- ============================================================

USE premier_league_db;

-- ============================================================
-- CLUBS
-- ============================================================
INSERT INTO Club (name, city, stadium, capacity, founded) VALUES
('Arsenal',                'London',     'Emirates Stadium',               60704, 1886),
('Chelsea',                'London',     'Stamford Bridge',                40853, 1905),
('Liverpool',              'Liverpool',  'Anfield',                        61276, 1892),
('Manchester City',        'Manchester', 'Etihad Stadium',                 55097, 1880),
('Manchester United',      'Manchester', 'Old Trafford',                   73812, 1878),
('Tottenham Hotspur',      'London',     'Tottenham Hotspur Stadium',      62850, 1882),
('Newcastle United',       'Newcastle',  'St. James Park',                 52258, 1892),
('Aston Villa',            'Birmingham', 'Villa Park',                     42657, 1874),
('West Ham United',        'London',     'London Stadium',                 60000, 1895),
('Brighton & Hove Albion', 'Brighton',   'Amex Stadium',                   31876, 1901);

-- ============================================================
-- COACHES
-- ============================================================
INSERT INTO Coach (first_name, last_name, nationality, date_of_birth, club_id, contract_start, contract_end) VALUES
('Mikel',   'Arteta',        'Spanish',    '1982-03-26', 1,  '2019-12-20', '2027-06-30'),
('Enzo',    'Maresca',       'Italian',    '1980-02-10', 2,  '2024-06-01', '2028-06-30'),
('Arne',    'Slot',          'Dutch',      '1978-09-17', 3,  '2024-06-01', '2027-06-30'),
('Pep',     'Guardiola',     'Spanish',    '1971-01-18', 4,  '2016-07-01', '2027-06-30'),
('Ruben',   'Amorim',        'Portuguese', '1985-01-27', 5,  '2024-11-11', '2027-06-30'),
('Ange',    'Postecoglou',   'Australian', '1965-08-27', 6,  '2023-06-06', '2026-06-30'),
('Eddie',   'Howe',          'English',    '1977-11-29', 7,  '2021-11-08', '2027-06-30'),
('Unai',    'Emery',         'Spanish',    '1971-11-03', 8,  '2022-10-26', '2027-06-30'),
('Julen',   'Lopetegui',     'Spanish',    '1966-08-28', 9,  '2024-06-12', '2026-06-30'),
('Fabian',  'Hurzeler',      'German',     '1993-01-15', 10, '2024-06-12', '2026-06-30');

-- ============================================================
-- PLAYERS
-- ============================================================
INSERT INTO Player (first_name, last_name, nationality, date_of_birth, position, jersey_number, club_id, market_value, contract_end) VALUES
-- Arsenal (club_id = 1)
('Bukayo',   'Saka',         'English',     '2001-09-05', 'Forward',    7,  1,  150.00, '2027-06-30'),
('Martin',   'Odegaard',     'Norwegian',   '1998-12-17', 'Midfielder', 8,  1,  100.00, '2028-06-30'),
('Gabriel',  'Magalhaes',    'Brazilian',   '1997-12-19', 'Defender',   6,  1,   80.00, '2027-06-30'),
('David',    'Raya',         'Spanish',     '1995-09-15', 'Goalkeeper', 22, 1,   35.00, '2027-06-30'),

-- Chelsea (club_id = 2)
('Cole',     'Palmer',       'English',     '2002-05-06', 'Midfielder', 20, 2,  150.00, '2033-06-30'),
('Nicolas',  'Jackson',      'Senegalese',  '2001-06-20', 'Forward',    15, 2,   70.00, '2031-06-30'),
('Reece',    'James',        'English',     '1999-12-08', 'Defender',   24, 2,   50.00, '2030-06-30'),
('Robert',   'Sanchez',      'Spanish',     '1997-11-18', 'Goalkeeper', 1,  2,   25.00, '2028-06-30'),

-- Liverpool (club_id = 3)
('Mohamed',  'Salah',        'Egyptian',    '1992-06-15', 'Forward',    11, 3,   70.00, '2026-06-30'),
('Virgil',   'van Dijk',     'Dutch',       '1991-07-08', 'Defender',   4,  3,   40.00, '2026-06-30'),
('Alexis',   'Mac Allister', 'Argentine',   '1998-12-24', 'Midfielder', 10, 3,   80.00, '2028-06-30'),
('Alisson',  'Becker',       'Brazilian',   '1992-10-02', 'Goalkeeper', 1,  3,   35.00, '2027-06-30'),

-- Manchester City (club_id = 4)
('Erling',   'Haaland',      'Norwegian',   '2000-07-21', 'Forward',    9,  4,  180.00, '2034-06-30'),
('Kevin',    'De Bruyne',    'Belgian',     '1991-06-28', 'Midfielder', 17, 4,   40.00, '2026-06-30'),
('Ruben',    'Dias',         'Portuguese',  '1997-05-14', 'Defender',   3,  4,   80.00, '2027-06-30'),
('Ederson',  'Moraes',       'Brazilian',   '1993-08-17', 'Goalkeeper', 31, 4,   40.00, '2026-06-30'),

-- Manchester United (club_id = 5)
('Bruno',    'Fernandes',    'Portuguese',  '1994-09-08', 'Midfielder', 8,  5,   70.00, '2026-06-30'),
('Marcus',   'Rashford',     'English',     '1997-10-31', 'Forward',    10, 5,   60.00, '2028-06-30'),
('Lisandro', 'Martinez',     'Argentine',   '1998-01-18', 'Defender',   6,  5,   55.00, '2028-06-30'),
('Andre',    'Onana',        'Cameroonian', '1996-04-02', 'Goalkeeper', 24, 5,   40.00, '2028-06-30'),

-- Tottenham Hotspur (club_id = 6)
('Heung-min','Son',          'South Korean','1992-07-08', 'Forward',    7,  6,   30.00, '2026-06-30'),
('James',    'Maddison',     'English',     '1996-11-23', 'Midfielder', 10, 6,   55.00, '2028-06-30'),
('Cristian', 'Romero',       'Argentine',   '1998-04-27', 'Defender',   17, 6,   75.00, '2028-06-30'),
('Guglielmo','Vicario',      'Italian',     '1996-10-07', 'Goalkeeper', 13, 6,   30.00, '2028-06-30'),

-- Newcastle United (club_id = 7)
('Alexander','Isak',         'Swedish',     '1999-09-21', 'Forward',    14, 7,  120.00, '2028-06-30'),
('Bruno',    'Guimaraes',    'Brazilian',   '1997-11-16', 'Midfielder', 39, 7,  100.00, '2028-06-30'),
('Kieran',   'Trippier',     'English',     '1990-09-19', 'Defender',   2,  7,   18.00, '2026-06-30'),
('Nick',     'Pope',         'English',     '1992-04-19', 'Goalkeeper', 22, 7,   22.00, '2027-06-30'),

-- Aston Villa (club_id = 8)
('Ollie',    'Watkins',      'English',     '1995-12-30', 'Forward',    11, 8,   80.00, '2028-06-30'),
('John',     'McGinn',       'Scottish',    '1994-10-18', 'Midfielder', 7,  8,   40.00, '2028-06-30'),
('Pau',      'Torres',       'Spanish',     '1997-01-16', 'Defender',   14, 8,   50.00, '2029-06-30'),
('Emiliano', 'Martinez',     'Argentine',   '1992-09-02', 'Goalkeeper', 1,  8,   35.00, '2027-06-30'),

-- West Ham United (club_id = 9)
('Jarrod',   'Bowen',        'English',     '1996-12-20', 'Forward',    20, 9,   55.00, '2030-06-30'),
('Lucas',    'Paqueta',      'Brazilian',   '1997-08-27', 'Midfielder', 11, 9,   55.00, '2028-06-30'),
('Aaron',    'Wan-Bissaka',  'English',     '1997-11-26', 'Defender',   2,  9,   25.00, '2028-06-30'),
('Lukasz',   'Fabianski',    'Polish',      '1985-04-18', 'Goalkeeper', 1,  9,    3.00, '2026-06-30'),

-- Brighton (club_id = 10)
('Joao',     'Pedro',        'Brazilian',   '2001-09-26', 'Forward',    9,  10,  60.00, '2028-06-30'),
('Carlos',   'Baleba',       'Cameroonian', '2003-09-03', 'Midfielder', 40, 10,  40.00, '2028-06-30'),
('Lewis',    'Dunk',         'English',     '1991-11-21', 'Defender',   5,  10,  15.00, '2026-06-30'),
('Bart',     'Verbruggen',   'Dutch',       '2002-08-18', 'Goalkeeper', 1,  10,  25.00, '2028-06-30');

-- ============================================================
-- MATCHES (2024/25 Season - Gameweeks 1-10)
-- ============================================================
INSERT INTO `Match` (home_club_id, away_club_id, match_date, home_score, away_score, season, gameweek) VALUES
-- Gameweek 1
(1, 6, '2024-08-17', 2, 1, '2024/25', 1),   -- Arsenal vs Tottenham
(3, 2, '2024-08-17', 2, 0, '2024/25', 1),   -- Liverpool vs Chelsea
(4, 5, '2024-08-18', 3, 1, '2024/25', 1),   -- Man City vs Man United
(7, 8, '2024-08-18', 1, 1, '2024/25', 1),   -- Newcastle vs Aston Villa
(9, 10,'2024-08-18', 2, 2, '2024/25', 1),   -- West Ham vs Brighton

-- Gameweek 2
(2, 1, '2024-08-24', 0, 1, '2024/25', 2),   -- Chelsea vs Arsenal
(5, 3, '2024-08-25', 0, 3, '2024/25', 2),   -- Man United vs Liverpool
(8, 4, '2024-08-25', 1, 2, '2024/25', 2),   -- Aston Villa vs Man City
(6, 7, '2024-08-25', 2, 1, '2024/25', 2),   -- Tottenham vs Newcastle
(10, 9,'2024-08-25', 1, 0, '2024/25', 2),   -- Brighton vs West Ham

-- Gameweek 3
(1, 3, '2024-09-01', 2, 2, '2024/25', 3),   -- Arsenal vs Liverpool
(4, 6, '2024-09-01', 4, 0, '2024/25', 3),   -- Man City vs Tottenham
(7, 2, '2024-09-01', 1, 2, '2024/25', 3),   -- Newcastle vs Chelsea
(8, 5, '2024-09-01', 3, 0, '2024/25', 3),   -- Aston Villa vs Man United
(9, 4, '2024-09-15', 0, 2, '2024/25', 4),   -- West Ham vs Man City

-- Gameweek 4-5
(3, 7, '2024-09-15', 3, 1, '2024/25', 4),   -- Liverpool vs Newcastle
(5, 10,'2024-09-15', 0, 1, '2024/25', 4),   -- Man United vs Brighton
(6, 8, '2024-09-22', 1, 2, '2024/25', 4),   -- Tottenham vs Aston Villa
(2, 4, '2024-09-22', 0, 1, '2024/25', 5),   -- Chelsea vs Man City
(1, 7, '2024-09-28', 4, 2, '2024/25', 5);   -- Arsenal vs Newcastle

-- ============================================================
-- PLAYER STATISTICS
-- ============================================================
INSERT INTO PlayerStatistics (player_id, match_id, goals, assists, yellow_cards, red_cards, minutes_played, shots_on_target, passes_completed) VALUES
-- Match 1: Arsenal(1) 2-1 Tottenham(6) | GW1
(1,  1, 1, 1, 0, 0, 90, 3, 42),  -- Saka
(2,  1, 1, 0, 0, 0, 90, 2, 78),  -- Odegaard
(3,  1, 0, 0, 1, 0, 90, 0, 62),  -- Gabriel
(21, 1, 1, 0, 0, 0, 90, 3, 35),  -- Son
(22, 1, 0, 1, 0, 0, 90, 1, 67),  -- Maddison

-- Match 2: Liverpool(3) 2-0 Chelsea(2) | GW1
(9,  2, 1, 1, 0, 0, 90, 4, 38),  -- Salah
(11, 2, 1, 0, 0, 0, 90, 2, 71),  -- Mac Allister
(10, 2, 0, 0, 0, 0, 90, 0, 58),  -- Van Dijk
(5,  2, 0, 0, 1, 0, 90, 1, 55),  -- Palmer

-- Match 3: Man City(4) 3-1 Man United(5) | GW1
(13, 3, 2, 0, 0, 0, 90, 5, 30),  -- Haaland
(14, 3, 1, 2, 0, 0, 90, 2, 88),  -- De Bruyne
(17, 3, 1, 0, 0, 0, 90, 2, 62),  -- B. Fernandes
(15, 3, 0, 0, 1, 0, 90, 0, 55),  -- Ruben Dias

-- Match 4: Newcastle(7) 1-1 Aston Villa(8) | GW1
(25, 4, 1, 0, 0, 0, 90, 3, 32),  -- Isak
(29, 4, 1, 1, 0, 0, 90, 2, 44),  -- O.Watkins
(26, 4, 0, 1, 0, 0, 90, 1, 76),  -- B.Guimaraes

-- Match 5: West Ham(9) 2-2 Brighton(10) | GW1
(33, 5, 1, 1, 0, 0, 90, 3, 45),  -- Bowen
(34, 5, 1, 0, 0, 0, 90, 2, 60),  -- Paqueta
(37, 5, 2, 0, 0, 0, 90, 4, 38),  -- J.Pedro

-- Match 6: Chelsea(2) 0-1 Arsenal(1) | GW2
(1,  6, 1, 0, 0, 0, 90, 3, 40),  -- Saka
(5,  6, 0, 0, 0, 0, 90, 2, 71),  -- Palmer
(6,  6, 0, 0, 1, 0, 90, 1, 42),  -- Jackson

-- Match 7: Man United(5) 0-3 Liverpool(3) | GW2
(9,  7, 2, 0, 0, 0, 90, 5, 40),  -- Salah
(11, 7, 1, 1, 0, 0, 90, 2, 75),  -- Mac Allister
(17, 7, 0, 0, 1, 0, 90, 1, 55),  -- B.Fernandes

-- Match 8: Aston Villa(8) 1-2 Man City(4) | GW2
(13, 8, 1, 0, 0, 0, 90, 4, 25),  -- Haaland
(14, 8, 1, 1, 0, 0, 90, 2, 90),  -- De Bruyne
(29, 8, 1, 0, 0, 0, 90, 3, 38),  -- Watkins

-- Match 9: Tottenham(6) 2-1 Newcastle(7) | GW2
(21, 9, 1, 0, 0, 0, 90, 3, 38),  -- Son
(22, 9, 1, 1, 0, 0, 90, 2, 72),  -- Maddison
(25, 9, 1, 0, 0, 0, 90, 3, 30),  -- Isak

-- Match 10: Brighton(10) 1-0 West Ham(9) | GW2
(37,10, 1, 0, 0, 0, 90, 3, 35),  -- J.Pedro

-- Match 11: Arsenal(1) 2-2 Liverpool(3) | GW3
(1, 11, 1, 1, 0, 0, 90, 4, 45),  -- Saka
(2, 11, 1, 0, 0, 0, 90, 2, 82),  -- Odegaard
(9, 11, 1, 0, 0, 0, 90, 3, 38),  -- Salah
(11,11, 1, 1, 0, 0, 90, 2, 70),  -- Mac Allister

-- Match 12: Man City(4) 4-0 Tottenham(6) | GW3
(13,12, 2, 0, 0, 0, 90, 6, 28),  -- Haaland
(14,12, 1, 3, 0, 0, 90, 1, 92),  -- De Bruyne
(1, 12, 0, 0, 0, 0,  0, 0,  0),  -- Saka (didn't play this match) -- removed, not in match 12

-- Match 13: Newcastle(7) 1-2 Chelsea(2) | GW3
(25,13, 1, 0, 0, 0, 90, 3, 30),  -- Isak
(5, 13, 1, 1, 0, 0, 90, 3, 75),  -- Palmer
(6, 13, 1, 0, 0, 0, 90, 2, 40),  -- Jackson

-- Match 14: Aston Villa(8) 3-0 Man United(5) | GW3
(29,14, 2, 0, 0, 0, 90, 5, 38),  -- Watkins
(30,14, 1, 1, 0, 0, 90, 1, 62),  -- McGinn
(17,14, 0, 0, 1, 0, 90, 1, 48),  -- B.Fernandes

-- Match 16: Liverpool(3) 3-1 Newcastle(7) | GW4
(9, 16, 2, 1, 0, 0, 90, 5, 42),  -- Salah
(11,16, 1, 0, 0, 0, 90, 2, 78),  -- Mac Allister
(25,16, 1, 0, 0, 0, 90, 2, 28),  -- Isak

-- Match 17: Man United(5) 0-1 Brighton(10) | GW4
(37,17, 1, 0, 0, 0, 90, 3, 35),  -- J.Pedro

-- Match 18: Tottenham(6) 1-2 Aston Villa(8) | GW4
(21,18, 1, 0, 0, 0, 90, 3, 40),  -- Son
(29,18, 1, 1, 0, 0, 90, 3, 42),  -- Watkins
(30,18, 1, 0, 0, 0, 90, 1, 60),  -- McGinn

-- Match 20: Arsenal(1) 4-2 Newcastle(7) | GW5
(1, 20, 2, 1, 0, 0, 90, 5, 50),  -- Saka
(2, 20, 1, 2, 0, 0, 90, 2, 85),  -- Odegaard
(3, 20, 1, 0, 0, 0, 90, 1, 70),  -- Gabriel
(25,20, 1, 0, 0, 0, 90, 3, 30),  -- Isak
(26,20, 1, 1, 0, 0, 90, 1, 65);  -- B.Guimaraes

-- ============================================================
-- TRANSFERS
-- ============================================================
INSERT INTO Transfer (player_id, from_club_id, to_club_id, transfer_date, transfer_fee, season) VALUES
(5,   4, 2,  '2023-07-05', 40.00, '2023/24'),  -- Cole Palmer: Man City → Chelsea
(21,  3, 6,  '2023-07-01', NULL,  '2023/24'),  -- Son renewed at Spurs (shown as re-signing)
(9,   NULL, 3,'2017-06-22', 42.00, '2017/18'), -- Salah: Roma → Liverpool
(13,  5, 4,  '2022-06-13', 51.20, '2022/23'), -- Haaland: Dortmund (via 5) → Man City
(25,  NULL, 7,'2022-08-04', 70.00, '2022/23'), -- Isak: Real Sociedad → Newcastle
(26,  NULL, 7,'2022-01-31', 40.00, '2022/23'), -- Guimaraes: Lyon → Newcastle
(34,  NULL, 9,'2023-06-30', 60.00, '2023/24'), -- Paqueta: Lyon → West Ham
(1,   NULL, 1,'2018-07-01', 2.50, '2018/19'),  -- Saka: Arsenal academy
(17,  NULL, 5,'2020-01-27', 55.00, '2019/20'), -- B.Fernandes: Sporting → Man United
(37,  NULL, 10,'2023-06-30', 30.00,'2023/24'); -- J.Pedro: Fluminense → Brighton

-- ============================================================
-- INJURIES
-- ============================================================
INSERT INTO Injury (player_id, injury_type, start_date, end_date, matches_missed) VALUES
(14, 'Knee Ligament',    '2024-08-20', NULL,         20),  -- De Bruyne (long term)
(10, 'Hamstring Strain', '2024-09-01', '2024-10-15',  6),  -- Van Dijk
(7,  'Knee Surgery',     '2024-07-15', NULL,         25),  -- Reece James (long term)
(22, 'Ankle Sprain',     '2024-09-10', '2024-10-20',  5),  -- Maddison
(30, 'Muscle Injury',    '2024-08-28', '2024-09-20',  3),  -- McGinn
(18, 'Achilles Tendon',  '2024-09-05', NULL,         15),  -- Rashford
(3,  'Calf Strain',      '2024-09-20', '2024-10-30',  4),  -- Gabriel
(35, 'Thigh Strain',     '2024-09-12', '2024-10-05',  4),  -- Wan-Bissaka
(26, 'Knee Bruise',      '2024-08-25', '2024-09-10',  2),  -- Guimaraes
(2,  'Back Problem',     '2024-10-01', NULL,          8);  -- Odegaard

-- ============================================================
-- LEAGUE STANDINGS (2024/25 Season - after 5 gameweeks)
-- ============================================================
INSERT INTO LeagueStandings (club_id, season, played, won, drawn, lost, goals_for, goals_against) VALUES
(1,  '2024/25', 5, 4, 1, 0, 12, 5),   -- Arsenal
(3,  '2024/25', 4, 3, 1, 0, 10, 3),   -- Liverpool
(4,  '2024/25', 4, 4, 0, 0, 10, 2),   -- Manchester City
(8,  '2024/25', 4, 3, 0, 1,  7, 5),   -- Aston Villa
(2,  '2024/25', 4, 2, 0, 2,  3, 5),   -- Chelsea
(6,  '2024/25', 4, 2, 0, 2,  4, 8),   -- Tottenham
(7,  '2024/25', 5, 1, 1, 3,  6, 12),  -- Newcastle
(10, '2024/25', 3, 2, 1, 0,  4, 2),   -- Brighton
(9,  '2024/25', 3, 0, 1, 2,  2, 4),   -- West Ham
(5,  '2024/25', 4, 0, 0, 4,  1, 10);  -- Manchester United
