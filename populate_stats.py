"""
Comprehensive Data Population Script
- PlayerStatistics for 2024/25 season (all 380 matches)
- Famous real transfers (2015-2025)
- Injury records (realistic)
- Fix minor club name issues
"""

import mysql.connector
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "123456",
    "database": "premier_league_db",
    "charset":  "utf8mb4",
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def qall(sql, p=()):
    c = get_conn(); cur = c.cursor(dictionary=True)
    cur.execute(sql, p); r = cur.fetchall(); cur.close(); c.close(); return r

def qone(sql, p=()):
    r = qall(sql, p); return r[0] if r else None

def run(sql, p=()):
    c = get_conn(); cur = c.cursor()
    cur.execute(sql, p); c.commit(); lid = cur.lastrowid; cur.close(); c.close(); return lid

def runmany(sql, data):
    c = get_conn(); cur = c.cursor()
    cur.executemany(sql, data); c.commit(); n = cur.rowcount; cur.close(); c.close(); return n


# ─────────────────────────────────────────────
# 1. FIX CLUB NAMES
# ─────────────────────────────────────────────
def fix_club_names():
    print("\n=== KULUP ADLARI DUZELTILIYOR ===")
    fixes = [
        ("Ipswich Town FC", "Ipswich Town"),
        ("Luton Town FC",   "Luton Town"),
    ]
    for old, new in fixes:
        r = qone("SELECT club_id FROM Club WHERE name=%s", (old,))
        if r:
            run("UPDATE Club SET name=%s WHERE name=%s", (new, old))
            print(f"  '{old}' -> '{new}'")


# ─────────────────────────────────────────────
# 2. ADD MISSING COACHES
# ─────────────────────────────────────────────
def add_coaches():
    print("\n=== EKSIK ANTRENORLER EKLENIYOR ===")
    coaches = [
        ("Andoni", "Iraola",     "Spanish",  "Bournemouth"),
        ("Marco",  "Silva",      "Portuguese","Fulham"),
        ("Kieran", "McKenna",    "Irish",     "Ipswich Town"),
        ("Rob",    "Edwards",    "Welsh",     "Luton Town"),
        ("Mark",   "Robins",     "English",   "Middlesbrough"),
    ]
    added = 0
    for fn, ln, nat, club_name in coaches:
        club = qone("SELECT club_id FROM Club WHERE name=%s", (club_name,))
        if not club:
            continue
        exists = qone("SELECT coach_id FROM Coach WHERE club_id=%s", (club["club_id"],))
        if not exists:
            run("INSERT INTO Coach (first_name,last_name,nationality,club_id) VALUES (%s,%s,%s,%s)",
                (fn, ln, nat, club["club_id"]))
            print(f"  + {fn} {ln} -> {club_name}")
            added += 1
    print(f"  {added} antrenor eklendi.")


# ─────────────────────────────────────────────
# 3. PLAYER STATISTICS (2024/25)
# ─────────────────────────────────────────────
def populate_player_stats():
    print("\n=== OYUNCU ISTATISTIKLERI OLUSTURULUYOR (2024/25) ===")

    matches = qall("""
        SELECT match_id, home_club_id, away_club_id, home_score, away_score
        FROM `Match` WHERE season='2024/25'
        ORDER BY match_id
    """)

    # Cache players per club {club_id: [player_ids]}
    all_players = qall("""
        SELECT player_id, club_id, position FROM Player
        WHERE position IN ('Forward','Midfielder','Defender','Goalkeeper')
    """)
    club_players = {}
    for p in all_players:
        cid = p["club_id"]
        if cid not in club_players:
            club_players[cid] = {"Forward":[], "Midfielder":[], "Defender":[], "Goalkeeper":[]}
        pos = p["position"] or "Midfielder"
        if pos in club_players[cid]:
            club_players[cid][pos].append(p["player_id"])

    stats_batch = []
    existing = set()
    ex_rows = qall("SELECT match_id, player_id FROM PlayerStatistics")
    for r in ex_rows:
        existing.add((r["match_id"], r["player_id"]))

    random.seed(42)

    def dist_goals(total, players_fw, players_mid):
        """Distribute goals among forwards/midfielders"""
        scorers = {}
        pool = players_fw * 3 + players_mid  # forwards 3x more likely
        for _ in range(total):
            if not pool:
                break
            scorer = random.choice(pool)
            scorers[scorer] = scorers.get(scorer, 0) + 1
        return scorers

    def dist_assists(scorers, players_fw, players_mid, players_def):
        """Each goal can have an assister (70% chance)"""
        assisters = {}
        all_pool = players_fw + players_mid * 2 + players_def
        for _ in range(sum(scorers.values())):
            if random.random() < 0.70 and all_pool:
                assister = random.choice(all_pool)
                assisters[assister] = assisters.get(assister, 0) + 1
        return assisters

    for m in matches:
        mid = m["match_id"]
        h_cid = m["home_club_id"]
        a_cid = m["away_club_id"]
        h_goals = m["home_score"]
        a_goals = m["away_score"]

        for cid, goals in [(h_cid, h_goals), (a_cid, a_goals)]:
            if cid not in club_players:
                continue
            fwd = club_players[cid]["Forward"]
            mid_p = club_players[cid]["Midfielder"]
            dfd = club_players[cid]["Defender"]
            gkp = club_players[cid]["Goalkeeper"]

            if not (fwd or mid_p):
                continue

            # Pick 11 starters + subs
            squad = []
            if gkp: squad += random.sample(gkp, min(1, len(gkp)))
            if dfd:  squad += random.sample(dfd,  min(4, len(dfd)))
            if mid_p: squad += random.sample(mid_p, min(4, len(mid_p)))
            if fwd:  squad += random.sample(fwd,  min(3, len(fwd)))
            # Fill up to 14 with subs
            all_avail = fwd + mid_p + dfd + gkp
            extras = [p for p in all_avail if p not in squad]
            squad += random.sample(extras, min(3, len(extras)))

            goal_dist   = dist_goals(goals, fwd, mid_p)
            assist_dist = dist_assists(goal_dist, fwd, mid_p, dfd)

            # Yellow cards: 1-2 per match per team
            yellow_players = random.sample(squad, min(random.randint(0, 2), len(squad)))
            red_player = random.choice(squad) if random.random() < 0.05 else None

            for pid in squad:
                if (mid, pid) in existing:
                    continue
                g  = goal_dist.get(pid, 0)
                a  = assist_dist.get(pid, 0)
                yc = 1 if pid in yellow_players else 0
                rc = 1 if pid == red_player else 0
                # GK plays 90min, subs less
                if pid in (gkp[:1] if gkp else []):
                    mins = 90
                elif pid in squad[:11]:
                    mins = random.randint(60, 90)
                else:
                    mins = random.randint(15, 45)
                sot = g + random.randint(0, 2) if pid in fwd + mid_p else 0
                stats_batch.append((pid, mid, g, a, yc, rc, mins, sot))
                existing.add((mid, pid))

    if stats_batch:
        n = runmany("""
            INSERT IGNORE INTO PlayerStatistics
                (player_id, match_id, goals, assists, yellow_cards, red_cards, minutes_played, shots_on_target)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, stats_batch)
        print(f"  {n} istatistik kaydi eklendi.")
    else:
        print("  Eklenecek istatistik yok.")


# ─────────────────────────────────────────────
# 4. FAMOUS TRANSFERS
# ─────────────────────────────────────────────
def add_transfers():
    print("\n=== UNLU TRANSFERLER EKLENIYOR ===")

    famous = [
        # (player_search, to_club_name, from_club_name, date, fee_M, season)
        ("Declan Rice",        "Arsenal",          "West Ham United",   "2023-07-15", 105.0, "2023/24"),
        ("Kai Havertz",        "Arsenal",          "Chelsea",           "2023-06-22",  65.0, "2023/24"),
        ("Moises Caicedo",     "Chelsea",          "Brighton & Hove Albion","2023-08-14",115.0, "2023/24"),
        ("Enzo Fernandez",     "Chelsea",          "Benfica",           "2023-01-27", 106.8, "2022/23"),
        ("Jack Grealish",      "Manchester City",  "Aston Villa",       "2021-08-05", 100.0, "2021/22"),
        ("Erling Haaland",     "Manchester City",  "Borussia Dortmund", "2022-06-13",  51.2, "2022/23"),
        ("Romelu Lukaku",      "Chelsea",          "Inter Milan",       "2021-08-12", 115.0, "2021/22"),
        ("Darwin Nunez",       "Liverpool",        "Benfica",           "2022-06-14",  67.7, "2022/23"),
        ("Virgil van Dijk",    "Liverpool",        "Southampton",       "2018-01-08",  75.0, "2017/18"),
        ("Alisson Becker",     "Liverpool",        "Roma",              "2018-07-19",  67.0, "2018/19"),
        ("Riyad Mahrez",       "Manchester City",  "Leicester City",    "2018-07-10",  60.0, "2018/19"),
        ("Leroy Sane",         "Manchester City",  "Schalke 04",        "2016-07-02",  37.0, "2016/17"),
        ("Benjamin Mendy",     "Manchester City",  "Monaco",            "2017-07-24",  52.0, "2017/18"),
        ("Raheem Sterling",    "Manchester City",  "Liverpool",         "2015-07-14",  49.0, "2015/16"),
        ("Alexis Sanchez",     "Manchester United","Arsenal",           "2018-01-22",   0.0, "2017/18"),
        ("Bruno Fernandes",    "Manchester United","Sporting CP",       "2020-01-30",  55.0, "2019/20"),
        ("Harry Maguire",      "Manchester United","Leicester City",    "2019-08-05",  80.0, "2019/20"),
        ("Paul Pogba",         "Manchester United","Juventus",          "2016-08-09",  89.0, "2016/17"),
        ("Jadon Sancho",       "Manchester United","Borussia Dortmund", "2021-07-23",  73.0, "2021/22"),
        ("Pedro Neto",         "Chelsea",          "Wolverhampton Wanderers","2024-07-10", 54.0, "2024/25"),
        ("Michael Olise",      "Bayern Munich",    "Crystal Palace",    "2024-07-02",  50.0, "2024/25"),
        ("Viktor Gyokeres",    "Arsenal",          "Sporting CP",       "2024-08-01",  63.0, "2024/25"),
        ("Noni Madueke",       "Arsenal",          "Chelsea",           "2025-01-14",  40.0, "2024/25"),
    ]

    added = 0
    for full_name, to_name, from_name, date, fee, season in famous:
        parts = full_name.split()
        fn = parts[0]; ln = " ".join(parts[1:])
        player = qone("SELECT player_id FROM Player WHERE first_name LIKE %s AND last_name LIKE %s LIMIT 1",
                      (f"%{fn}%", f"%{ln}%"))
        if not player:
            player = qone("SELECT player_id FROM Player WHERE last_name LIKE %s LIMIT 1", (f"%{ln}%",))
        if not player:
            print(f"  [!] Oyuncu bulunamadi: {full_name}")
            continue

        to_club   = qone("SELECT club_id FROM Club WHERE name=%s", (to_name,))
        from_club = qone("SELECT club_id FROM Club WHERE name=%s", (from_name,))

        if not to_club:
            print(f"  [!] Hedef kulup bulunamadi: {to_name}")
            continue

        fee_val = fee * 1_000_000 if fee > 0 else None
        from_id = from_club["club_id"] if from_club else None
        run("""
            INSERT INTO Transfer (player_id, from_club_id, to_club_id, transfer_date, transfer_fee, season)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (player["player_id"], from_id, to_club["club_id"], date, fee_val, season))
        print(f"  + {full_name} -> {to_name} ({season}, £{fee}M)")
        added += 1

    print(f"  Toplam {added} transfer eklendi.")


# ─────────────────────────────────────────────
# 5. INJURIES
# ─────────────────────────────────────────────
def add_injuries():
    print("\n=== SAKATLIK KAYITLARI EKLENIYOR ===")

    injury_data = [
        # (player_search, injury_type, start, end, missed)
        ("Bukayo Saka",       "Hamstring",        "2024-12-22", None,         8),
        ("Martin Odegaard",   "Ankle",            "2024-09-05", "2024-10-28", 12),
        ("Declan Rice",       "Suspension",       "2025-01-20", "2025-02-05", 3),
        ("Rodri",             "ACL",              "2024-09-22", None,         35),
        ("Kevin De Bruyne",   "Muscle",           "2024-10-15", "2024-12-20", 10),
        ("Erling Haaland",    "Ankle",            "2024-11-05", "2024-12-01", 6),
        ("Ollie Watkins",     "Knee",             "2025-01-12", "2025-02-20", 5),
        ("Mohamed Salah",     "Hamstring",        "2025-02-08", None,         4),
        ("Virgil van Dijk",   "Knock",            "2024-09-10", "2024-09-25", 2),
        ("Bruno Fernandes",   "Suspension",       "2025-03-01", "2025-03-15", 2),
        ("Marcus Rashford",   "Muscle",           "2024-12-10", "2025-01-15", 5),
        ("Reece James",       "Hamstring",        "2024-11-20", None,         14),
        ("Ben Chilwell",      "Knee",             "2024-10-05", "2025-01-01", 12),
        ("Trent Alexander-Arnold","Muscle",       "2024-10-20", "2024-11-15", 4),
        ("Son Heung-min",     "Ankle",            "2025-01-25", "2025-02-15", 3),
        ("James Maddison",    "Knee",             "2024-12-01", "2025-01-20", 7),
        ("Dominic Calvert-Lewin","Hamstring",     "2024-11-10", "2024-12-20", 5),
        ("Kalvin Phillips",   "Muscle",           "2024-09-15", "2024-10-10", 3),
        ("Ederson",           "Rib",              "2025-02-20", None,         6),
        ("Alisson Becker",    "Shoulder",         "2024-12-28", "2025-02-01", 5),
    ]

    added = 0
    for full_name, inj_type, start, end, missed in injury_data:
        parts = full_name.split()
        fn = parts[0]; ln = " ".join(parts[1:])
        player = qone("SELECT player_id FROM Player WHERE first_name LIKE %s AND last_name LIKE %s LIMIT 1",
                      (f"%{fn}%", f"%{ln}%"))
        if not player:
            player = qone("SELECT player_id FROM Player WHERE last_name LIKE %s LIMIT 1", (f"%{ln}%",))
        if not player:
            print(f"  [!] Oyuncu bulunamadi: {full_name}")
            continue

        run("INSERT INTO Injury (player_id, injury_type, start_date, end_date, matches_missed) VALUES (%s,%s,%s,%s,%s)",
            (player["player_id"], inj_type, start, end, missed))
        print(f"  + {full_name}: {inj_type} ({start})")
        added += 1

    print(f"  Toplam {added} sakatlık eklendi.")


# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
def summary():
    print("\n" + "="*55)
    print("  VERI TABANI OZETI")
    print("="*55)
    tables = [("Club","Club"),("Coach","Coach"),("Player","Player"),
              ("Match","\\`Match\\`"),("PlayerStatistics","PlayerStatistics"),
              ("Transfer","Transfer"),("Injury","Injury"),("LeagueStandings","LeagueStandings")]
    for label, tbl in tables:
        r = qone(f"SELECT COUNT(*) AS n FROM {tbl}")
        print(f"  {label:<20}: {r['n']:>6}")

    print("\n  Sezon Sampiyon Ozeti:")
    champs = qall("""
        SELECT ls.season, c.name, (ls.won*3+ls.drawn) AS pts
        FROM LeagueStandings ls JOIN Club c ON ls.club_id=c.club_id
        WHERE (ls.won*3+ls.drawn) = (
            SELECT MAX(ls2.won*3+ls2.drawn) FROM LeagueStandings ls2 WHERE ls2.season=ls.season)
        ORDER BY ls.season
    """)
    for r in champs:
        print(f"    {r['season']}: {r['name']:<30} {r['pts']} puan")

    print("\n  Top 10 Gol Krali (2024/25):")
    scorers = qall("""
        SELECT CONCAT(p.first_name,' ',p.last_name) AS player, c.name AS club,
               SUM(ps.goals) AS goals, SUM(ps.assists) AS assists
        FROM PlayerStatistics ps
        JOIN Player p ON ps.player_id=p.player_id
        JOIN `Match` m ON ps.match_id=m.match_id
        LEFT JOIN Club c ON p.club_id=c.club_id
        WHERE m.season='2024/25'
        GROUP BY p.player_id
        ORDER BY goals DESC, assists DESC
        LIMIT 10
    """)
    for i, r in enumerate(scorers, 1):
        print(f"    {i:2}. {r['player']:<28} {r['club']:<22} {r['goals']} gol {r['assists']} asist")


if __name__ == "__main__":
    fix_club_names()
    add_coaches()
    populate_player_stats()
    add_transfers()
    add_injuries()
    summary()
    print("\nTamamlandi!")
