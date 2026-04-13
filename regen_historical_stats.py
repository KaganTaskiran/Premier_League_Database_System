"""
Regenerate PlayerStatistics for all seasons with realistic goal distribution.
- Keeps existing match-player associations (who played in which match)
- Resets goals/assists to 0 then redistributes realistically
- Real top scorers get their actual season goal counts
- Total season goals ~900-1100 (realistic PL average)
"""
import mysql.connector
import random
import unicodedata
from collections import defaultdict

DB = dict(host='localhost', user='root', password='123456', database='premier_league_db')

def conn():
    return mysql.connector.connect(**DB)

def normalize(s):
    if not s:
        return ''
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower().strip()

# Real top scorers per season: normalized full name -> goals
REAL_GOALS = {
    '2015/16': {
        'harry kane': 25, 'romelu lukaku': 25, 'sergio aguero': 24,
        'jamie vardy': 24, 'riyad mahrez': 17, 'olivier giroud': 16,
        'alexis sanchez': 15, 'sadio mane': 11, 'roberto firmino': 10,
        'dele alli': 10, 'wayne rooney': 8, 'christian eriksen': 6,
        'eden hazard': 5, 'raheem sterling': 6, 'sergio kun aguero': 24,
    },
    '2016/17': {
        'harry kane': 29, 'romelu lukaku': 25, 'alexis sanchez': 24,
        'diego costa': 20, 'sergio aguero': 20, 'dele alli': 18,
        'zlatan ibrahimovic': 17, 'jermain defoe': 15, 'eden hazard': 16,
        'roberto firmino': 12, 'heung-min son': 14, 'sadio mane': 13,
        'raheem sterling': 7, 'kevin de bruyne': 6,
    },
    '2017/18': {
        'mohamed salah': 32, 'harry kane': 30, 'sergio aguero': 21,
        'alexandre lacazette': 14, 'raheem sterling': 18, 'roberto firmino': 15,
        'leroy sane': 10, 'sadio mane': 10, 'eden hazard': 12,
        'jamie vardy': 20, 'marcus rashford': 7, 'heung-min son': 12,
        'alvaro morata': 11, 'pierre-emerick aubameyang': 10,
    },
    '2018/19': {
        'pierre-emerick aubameyang': 22, 'sadio mane': 22, 'mohamed salah': 22,
        'sergio aguero': 21, 'harry kane': 17, 'jamie vardy': 18,
        'raheem sterling': 17, 'eden hazard': 16, 'callum wilson': 14,
        'raul jimenez': 13, 'glenn murray': 13, 'roberto firmino': 12,
        'heung-min son': 12,
    },
    '2019/20': {
        'jamie vardy': 23, 'danny ings': 22, 'pierre-emerick aubameyang': 22,
        'sergio aguero': 23, 'raheem sterling': 20, 'harry kane': 18,
        'sadio mane': 18, 'mohamed salah': 19, 'marcus rashford': 17,
        'dominic calvert-lewin': 13, 'heung-min son': 11, 'tammy abraham': 15,
    },
    '2020/21': {
        'harry kane': 23, 'mohamed salah': 22, 'bruno fernandes': 18,
        'dominic calvert-lewin': 16, 'heung-min son': 17, 'patrick bamford': 17,
        'ollie watkins': 14, 'jamie vardy': 15, 'callum wilson': 12,
        'sadio mane': 11, 'riyad mahrez': 9, 'marcus rashford': 11,
        'gabriel jesus': 9,
    },
    '2021/22': {
        'mohamed salah': 23, 'heung-min son': 23, 'riyad mahrez': 24,
        'cristiano ronaldo': 18, 'diogo jota': 15, 'kevin de bruyne': 15,
        'harry kane': 17, 'jarrod bowen': 12, 'bukayo saka': 11,
        'raheem sterling': 13, 'sadio mane': 16, 'bernardo silva': 8,
        'Bruno Fernandes': 10,
    },
    '2022/23': {
        'erling haaland': 36, 'harry kane': 30, 'ivan toney': 20,
        'callum wilson': 18, 'marcus rashford': 17, 'mohamed salah': 19,
        'martin odegaard': 15, 'bukayo saka': 14, 'leandro trossard': 7,
        'heung-min son': 10, 'gabriel martinelli': 15, 'kevin de bruyne': 7,
        'rodrigo moreno': 14,
    },
    '2023/24': {
        'erling haaland': 27, 'cole palmer': 22, 'alexander isak': 21,
        'ollie watkins': 19, 'dominic solanke': 19, 'phil foden': 19,
        'jarrod bowen': 16, 'bukayo saka': 16, 'heung-min son': 17,
        'mohamed salah': 18, 'leandro trossard': 14, 'richarlison': 10,
    },
    '2024/25': {
        'mohamed salah': 29, 'erling haaland': 22, 'alexander isak': 21,
        'cole palmer': 20, 'chris wood': 20, 'liam delap': 16,
        'bukayo saka': 15, 'heung-min son': 14, 'dominic solanke': 14,
        'ollie watkins': 13, 'gabriel martinelli': 11, 'marcus rashford': 11,
        'phil foden': 10, 'martin odegaard': 8, 'virgil van dijk': 4,
    },
}

# Season goal targets (total goals for the season across all players)
SEASON_GOAL_TARGETS = {
    '2015/16': 1026, '2016/17': 1064, '2017/18': 1018,
    '2018/19': 1072, '2019/20': 1034, '2020/21': 1024,
    '2021/22': 1071, '2022/23': 1084, '2023/24': 1107,
    '2024/25': 1100,
}

def get_season_data(season):
    """Get all (player_id, match_id, club_id, position, market_value, fullname) for a season."""
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("""
        SELECT ps.player_id, ps.match_id,
               CASE WHEN m.home_club_id IN (
                   SELECT club_id FROM Player p2 WHERE p2.player_id=ps.player_id
               ) THEN m.home_club_id ELSE m.away_club_id END AS club_id,
               p.position,
               COALESCE(p.market_value, 1.0) AS market_value,
               CONCAT(LOWER(p.first_name),' ',LOWER(p.last_name)) AS fullname,
               p.first_name, p.last_name
        FROM PlayerStatistics ps
        JOIN Player p ON ps.player_id = p.player_id
        JOIN `Match` m ON ps.match_id = m.match_id
        WHERE m.season = %s
    """, (season,))
    rows = cur.fetchall()
    cur.close()
    c.close()
    return rows

def get_season_data_v2(season):
    """Get all PlayerStatistics records for a season with player info."""
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("""
        SELECT ps.player_id, ps.match_id, ps.minutes_played,
               p.position,
               COALESCE(p.market_value, 1.0) AS market_value,
               LOWER(CONCAT(COALESCE(p.first_name,''),' ',COALESCE(p.last_name,''))) AS fullname
        FROM PlayerStatistics ps
        JOIN Player p ON ps.player_id = p.player_id
        JOIN `Match` m ON ps.match_id = m.match_id
        WHERE m.season = %s
    """, (season,))
    rows = cur.fetchall()
    cur.close()
    c.close()
    return rows

def get_matches_for_season(season):
    """Get all match_ids and goal totals per match for a season."""
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("""
        SELECT match_id, home_score, away_score,
               (home_score + away_score) AS total_goals
        FROM `Match` WHERE season = %s
    """, (season,))
    rows = cur.fetchall()
    cur.close()
    c.close()
    return rows

def build_player_weights(records, real_goals_for_season):
    """
    Build target goals for each player_id.
    Real players get their target, others get weighted random allocation.
    """
    # Group records by player
    player_info = {}  # player_id -> {position, market_value, fullname, match_ids}
    for r in records:
        pid = r['player_id']
        if pid not in player_info:
            player_info[pid] = {
                'position': r['position'],
                'market_value': float(r['market_value'] or 1.0),
                'fullname': normalize(r['fullname']),
                'match_ids': [],
            }
        player_info[pid]['match_ids'].append(r['match_id'])

    # Match real players
    name_to_pid = {}
    for pid, info in player_info.items():
        name_to_pid[info['fullname']] = pid

    # Assign real goals
    real_assignments = {}
    matched_names = set()
    for name, goals in real_goals_for_season.items():
        norm_name = normalize(name)
        # Exact match
        if norm_name in name_to_pid:
            pid = name_to_pid[norm_name]
            real_assignments[pid] = goals
            matched_names.add(norm_name)
            continue
        # Partial match (last name)
        parts = norm_name.split()
        if len(parts) >= 2:
            last = parts[-1]
            for pname, pid in name_to_pid.items():
                if last in pname and pname not in matched_names:
                    real_assignments[pid] = goals
                    matched_names.add(pname)
                    break

    return player_info, real_assignments

def position_weight(pos, mv):
    """Base scoring weight by position and market value."""
    base = max(mv, 0.5)
    if pos == 'Forward':
        return base * 3.0
    elif pos == 'Midfielder':
        return base * 1.2
    elif pos == 'Defender':
        return base * 0.3
    else:  # Goalkeeper
        return base * 0.05

def distribute_goals_for_season(season, records, real_goals_for_season, total_goal_target):
    """
    Returns dict: {(player_id, match_id): (goals, assists)}
    """
    player_info, real_assignments = build_player_weights(records, real_goals_for_season)

    # Build per-match player lists
    match_players = defaultdict(list)  # match_id -> [player_id, ...]
    for r in records:
        match_players[r['match_id']].append(r['player_id'])

    # Get match goal totals from Match table
    match_goals = {}
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("""
        SELECT match_id, (home_score+away_score) AS total
        FROM `Match` WHERE season=%s
    """, (season,))
    for row in cur.fetchall():
        match_goals[row['match_id']] = row['total']
    cur.close()
    c.close()

    # Determine total real-assigned goals
    real_total = sum(real_assignments.values())

    # We need total_goal_target goals in total
    # If real_total > total_goal_target, cap it
    if real_total > total_goal_target:
        # Scale down real assignments proportionally
        factor = total_goal_target / real_total * 0.9
        real_assignments = {pid: max(1, int(g * factor)) for pid, g in real_assignments.items()}
        real_total = sum(real_assignments.values())

    remaining_goals = total_goal_target - real_total

    # Non-real players' weights
    non_real_players = [pid for pid in player_info if pid not in real_assignments]
    weights = {}
    for pid in non_real_players:
        info = player_info[pid]
        weights[pid] = position_weight(info['position'], info['market_value'])

    total_weight = sum(weights.values()) or 1

    # Distribute remaining goals weighted
    player_target_goals = dict(real_assignments)
    for pid in non_real_players:
        share = (weights[pid] / total_weight) * remaining_goals
        player_target_goals[pid] = int(share)

    # Now distribute per match using match actual scores
    result = {}  # (player_id, match_id) -> (goals, assists, yellow, red, mins)

    # Track remaining per player
    player_remaining = defaultdict(int, player_target_goals)
    # Also track assist allocation (assists ~ 80% of goals)
    player_assist_target = {pid: int(g * 0.75) for pid, g in player_target_goals.items()}
    player_assists_remaining = defaultdict(int, player_assist_target)

    # Initialize all to 0
    for r in records:
        key = (r['player_id'], r['match_id'])
        mins = r.get('minutes_played', 0) or random.randint(60, 90)
        yc = random.choices([0, 1], weights=[85, 15])[0]
        rc = random.choices([0, 1], weights=[98, 2])[0] if yc == 0 else 0
        result[key] = [0, 0, yc, rc, mins]

    # For each match, distribute goals among players based on their targets
    match_list = list(match_players.keys())
    random.shuffle(match_list)

    for match_id in match_list:
        players_in_match = match_players[match_id]
        goals_this_match = match_goals.get(match_id, 2)
        assists_this_match = goals_this_match  # 1 assist per goal

        # Assign goals
        for _ in range(goals_this_match):
            # Build weights for scorers in this match
            eligible = [p for p in players_in_match if player_remaining[p] > 0]
            if not eligible:
                eligible = players_in_match
            w = []
            for p in eligible:
                info = player_info.get(p, {})
                base = position_weight(info.get('position', 'Forward'), info.get('market_value', 1.0))
                w.append(base * (1 + player_remaining[p]))
            if not any(x > 0 for x in w):
                w = [1] * len(eligible)
            scorer = random.choices(eligible, weights=w, k=1)[0]
            result[(scorer, match_id)][0] += 1
            player_remaining[scorer] = max(0, player_remaining[scorer] - 1)

        # Assign assists
        for _ in range(min(assists_this_match, goals_this_match)):
            eligible = [p for p in players_in_match if player_assists_remaining[p] > 0]
            if not eligible:
                eligible = players_in_match
            w = []
            for p in eligible:
                info = player_info.get(p, {})
                base = position_weight(info.get('position', 'Midfielder'), info.get('market_value', 1.0))
                w.append(base * (1 + player_assists_remaining[p]))
            if not any(x > 0 for x in w):
                w = [1] * len(eligible)
            assister = random.choices(eligible, weights=w, k=1)[0]
            result[(assister, match_id)][1] += 1
            player_assists_remaining[assister] = max(0, player_assists_remaining[assister] - 1)

    return result

def regen_season(season):
    print(f"\n{'='*50}")
    print(f"Processing {season}...")

    records = get_season_data_v2(season)
    if not records:
        print(f"  No records found for {season}, skipping.")
        return

    print(f"  Found {len(records)} existing stat records")
    real_goals = REAL_GOALS.get(season, {})
    total_target = SEASON_GOAL_TARGETS.get(season, 1050)

    result = distribute_goals_for_season(season, records, real_goals, total_target)

    # Batch update
    c = conn()
    cur = c.cursor()

    updates = []
    for (player_id, match_id), (goals, assists, yc, rc, mins) in result.items():
        updates.append((goals, assists, yc, rc, mins, player_id, match_id))

    cur.executemany("""
        UPDATE PlayerStatistics
        SET goals=%s, assists=%s, yellow_cards=%s, red_cards=%s, minutes_played=%s
        WHERE player_id=%s AND match_id=%s
    """, updates)
    c.commit()

    updated = cur.rowcount
    total_goals = sum(v[0] for v in result.values())
    total_assists = sum(v[1] for v in result.values())
    print(f"  Updated {len(updates)} records")
    print(f"  Total goals: {total_goals} (target: {total_target})")
    print(f"  Total assists: {total_assists}")

    # Show top 5 scorers
    cur2 = c.cursor(dictionary=True)
    cur2.execute("""
        SELECT CONCAT(p.first_name,' ',p.last_name) AS oyuncu,
               COALESCE(c.name,'Free Agent') AS kulup,
               SUM(ps.goals) AS goller
        FROM PlayerStatistics ps
        JOIN Player p ON ps.player_id=p.player_id
        JOIN `Match` m ON ps.match_id=m.match_id
        LEFT JOIN Club c ON p.club_id=c.club_id
        WHERE m.season=%s
        GROUP BY ps.player_id
        ORDER BY goller DESC LIMIT 5
    """, (season,))
    print(f"  Top scorers:")
    for row in cur2.fetchall():
        print(f"    {row['oyuncu']:25s} ({row['kulup']:20s}) {row['goller']} goals")

    cur.close()
    cur2.close()
    c.close()

if __name__ == '__main__':
    seasons = [
        '2015/16', '2016/17', '2017/18', '2018/19', '2019/20',
        '2020/21', '2021/22', '2022/23', '2023/24', '2024/25',
    ]
    for s in seasons:
        regen_season(s)
    print("\nDone! All seasons regenerated.")
