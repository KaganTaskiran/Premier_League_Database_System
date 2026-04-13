"""
Premier League Data Fetcher v2 — OpenFootball + football-data.org
SE 2230: Database Systems - Yaşar University 2026

Veri kaynakları:
  - github.com/openfootball/football.json  (KEY GEREKMİYOR - 3800+ mac)
  - api.football-data.org                  (Guncel kadro - gunluk 10 istek)

KULLANIM: python fetch_data.py
"""

import requests
import mysql.connector
import sys
import io
import time

# Windows konsolunda UTF-8 zorla
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ──────────────────────────────────────────
# AYARLAR
# ──────────────────────────────────────────
FD_API_KEY = "3b1a4469d6b045ebb39fb65ed0ce8cac"   # football-data.org (kadro icin)

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "bbb0",
    "database": "premier_league_db",
    "charset":  "utf8mb4",
}

# OpenFootball JSON URL'leri
OFB_BASE = "https://raw.githubusercontent.com/openfootball/football.json/master"
SEASONS = [
    ("2015-16", "2015/16"),
    ("2016-17", "2016/17"),
    ("2017-18", "2017/18"),
    ("2018-19", "2018/19"),
    ("2019-20", "2019/20"),
    ("2020-21", "2020/21"),
    ("2021-22", "2021/22"),
    ("2022-23", "2022/23"),
    ("2023-24", "2023/24"),
    ("2024-25", "2024/25"),
]

# ──────────────────────────────────────────
# DB YARDIMCILARI
# ──────────────────────────────────────────
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def qone(sql, p=()):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, p); row = cur.fetchone()
    cur.close(); conn.close(); return row

def qall(sql, p=()):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, p); rows = cur.fetchall()
    cur.close(); conn.close(); return rows

def run(sql, p=()):
    conn = get_db(); cur = conn.cursor()
    cur.execute(sql, p); conn.commit(); lid = cur.lastrowid
    cur.close(); conn.close(); return lid

# Kulup adi normalizasyon (OpenFootball isimleri cesitli olabiliyor)
CLUB_ALIASES = {
    # Arsenal
    "Arsenal":                      "Arsenal",
    "Arsenal FC":                   "Arsenal",
    # Aston Villa
    "Aston Villa":                  "Aston Villa",
    "Aston Villa FC":               "Aston Villa",
    # Bournemouth
    "Bournemouth":                  "Bournemouth",
    "AFC Bournemouth":              "Bournemouth",
    # Brentford
    "Brentford":                    "Brentford",
    "Brentford FC":                 "Brentford",
    # Brighton
    "Brighton & Hove Albion":       "Brighton & Hove Albion",
    "Brighton & Hove Albion FC":    "Brighton & Hove Albion",
    "Brighton and Hove Albion":     "Brighton & Hove Albion",
    "Brighton Hove":                "Brighton & Hove Albion",
    "Brighton":                     "Brighton & Hove Albion",
    # Burnley
    "Burnley":                      "Burnley",
    "Burnley FC":                   "Burnley",
    # Cardiff
    "Cardiff City":                 "Cardiff City",
    "Cardiff City FC":              "Cardiff City",
    "Cardiff":                      "Cardiff City",
    # Chelsea
    "Chelsea":                      "Chelsea",
    "Chelsea FC":                   "Chelsea",
    # Crystal Palace
    "Crystal Palace":               "Crystal Palace",
    "Crystal Palace FC":            "Crystal Palace",
    # Everton
    "Everton":                      "Everton",
    "Everton FC":                   "Everton",
    # Fulham
    "Fulham":                       "Fulham",
    "Fulham FC":                    "Fulham",
    # Huddersfield
    "Huddersfield Town":            "Huddersfield Town",
    "Huddersfield Town FC":         "Huddersfield Town",
    "Huddersfield":                 "Huddersfield Town",
    # Hull
    "Hull City":                    "Hull City",
    "Hull City FC":                 "Hull City",
    "Hull":                         "Hull City",
    # Ipswich
    "Ipswich Town":                 "Ipswich Town",
    "Ipswich Town FC":              "Ipswich Town",
    "Ipswich":                      "Ipswich Town",
    # Leeds United
    "Leeds United":                 "Leeds United",
    "Leeds United FC":              "Leeds United",
    "Leeds":                        "Leeds United",
    # Leicester City
    "Leicester City":               "Leicester City",
    "Leicester City FC":            "Leicester City",
    "Leicester":                    "Leicester City",
    # Liverpool
    "Liverpool":                    "Liverpool",
    "Liverpool FC":                 "Liverpool",
    # Luton
    "Luton Town":                   "Luton Town",
    "Luton Town FC":                "Luton Town",
    "Luton":                        "Luton Town",
    # Manchester City
    "Manchester City":              "Manchester City",
    "Manchester City FC":           "Manchester City",
    "Man City":                     "Manchester City",
    # Manchester United
    "Manchester United":            "Manchester United",
    "Manchester United FC":         "Manchester United",
    "Man United":                   "Manchester United",
    "Man Utd":                      "Manchester United",
    # Middlesbrough
    "Middlesbrough":                "Middlesbrough",
    "Middlesbrough FC":             "Middlesbrough",
    # Newcastle United
    "Newcastle United":             "Newcastle United",
    "Newcastle United FC":          "Newcastle United",
    "Newcastle":                    "Newcastle United",
    # Norwich City
    "Norwich City":                 "Norwich City",
    "Norwich City FC":              "Norwich City",
    "Norwich":                      "Norwich City",
    # Nottingham Forest
    "Nottingham Forest":            "Nottingham Forest",
    "Nottingham Forest FC":         "Nottingham Forest",
    "Nott'm Forest":                "Nottingham Forest",
    "Nottingham":                   "Nottingham Forest",
    # Sheffield United
    "Sheffield United":             "Sheffield United",
    "Sheffield United FC":          "Sheffield United",
    "Sheffield Utd":                "Sheffield United",
    # Southampton
    "Southampton":                  "Southampton",
    "Southampton FC":               "Southampton",
    # Sunderland
    "Sunderland":                   "Sunderland",
    "Sunderland AFC":               "Sunderland",
    # Swansea
    "Swansea City":                 "Swansea City",
    "Swansea City AFC":             "Swansea City",
    "Swansea":                      "Swansea City",
    # Tottenham Hotspur
    "Tottenham Hotspur":            "Tottenham Hotspur",
    "Tottenham Hotspur FC":         "Tottenham Hotspur",
    "Tottenham":                    "Tottenham Hotspur",
    "Spurs":                        "Tottenham Hotspur",
    # Watford
    "Watford":                      "Watford",
    "Watford FC":                   "Watford",
    # West Brom
    "West Bromwich Albion":         "West Bromwich Albion",
    "West Bromwich Albion FC":      "West Bromwich Albion",
    "West Brom":                    "West Bromwich Albion",
    # West Ham United
    "West Ham United":              "West Ham United",
    "West Ham United FC":           "West Ham United",
    "West Ham":                     "West Ham United",
    # Wolverhampton Wanderers
    "Wolverhampton Wanderers":      "Wolverhampton Wanderers",
    "Wolverhampton Wanderers FC":   "Wolverhampton Wanderers",
    "Wolverhampton":                "Wolverhampton Wanderers",
    "Wolves":                       "Wolverhampton Wanderers",
}

def normalize_club(name):
    return CLUB_ALIASES.get(name, name)

def get_or_create_club(name):
    norm = normalize_club(name)
    row = qone("SELECT club_id FROM Club WHERE name = %s", (norm,))
    if row:
        return row["club_id"]
    cid = run("INSERT INTO Club (name, city, stadium, capacity, founded) VALUES (%s,'England','Unknown Stadium',NULL,NULL)", (norm,))
    print(f"  [+] Yeni kulup: {norm}")
    return cid

# ──────────────────────────────────────────
# BOLUM 1: MACLAR (OpenFootball)
# ──────────────────────────────────────────
def fetch_matches():
    print("\n=== MACLAR CEKILIYOR (OpenFootball) ===")
    total_new = 0

    for folder, season_str in SEASONS:
        url = f"{OFB_BASE}/{folder}/en.1.json"
        print(f"  {season_str} -> {url}")
        try:
            r = requests.get(url, timeout=30)
            if r.status_code != 200:
                print(f"  HATA {r.status_code}, atlaniyor.")
                continue
            data = r.json()
        except Exception as e:
            print(f"  HATA: {e}")
            continue

        rounds = data.get("rounds", data.get("matches", []))
        season_new = 0

        for rd in rounds:
            # round objesi ya da duz match listesi olabilir
            matches = rd.get("matches", [rd]) if isinstance(rd, dict) and "matches" in rd else [rd]
            gw_name = rd.get("name", "") if isinstance(rd, dict) else ""
            try:
                gw_num = int(''.join(filter(str.isdigit, gw_name))) if gw_name else None
            except:
                gw_num = None

            for m in matches:
                if not isinstance(m, dict):
                    continue

                date = m.get("date") or m.get("utcDate", "")
                if not date or len(date) < 10:
                    continue
                date = date[:10]

                # Takim isimleri (farkli formatlarda gelebilir)
                t1 = m.get("team1") or m.get("homeTeam") or {}
                t2 = m.get("team2") or m.get("awayTeam") or {}
                if isinstance(t1, str): t1 = {"name": t1}
                if isinstance(t2, str): t2 = {"name": t2}
                home_name = t1.get("name") or t1.get("shortName", "")
                away_name = t2.get("name") or t2.get("shortName", "")
                if not home_name or not away_name:
                    continue

                home_id = get_or_create_club(home_name)
                away_id = get_or_create_club(away_name)
                if home_id == away_id:
                    continue

                # Skor
                score = m.get("score") or {}
                if isinstance(score, str):
                    # "2:1" formatı
                    parts = score.replace("-", ":").split(":")
                    try:
                        hs, as_ = int(parts[0].strip()), int(parts[1].strip())
                    except:
                        hs, as_ = 0, 0
                elif isinstance(score, dict):
                    ft = score.get("ft") or score.get("fullTime") or {}
                    if isinstance(ft, list) and len(ft) >= 2:
                        hs, as_ = int(ft[0] or 0), int(ft[1] or 0)
                    elif isinstance(ft, dict):
                        hs = ft.get("home") or ft.get("homeTeam") or 0
                        as_ = ft.get("away") or ft.get("awayTeam") or 0
                    else:
                        hs, as_ = 0, 0
                else:
                    hs, as_ = 0, 0

                # Zaten var mi?
                ex = qone(
                    "SELECT match_id FROM `Match` WHERE home_club_id=%s AND away_club_id=%s AND match_date=%s",
                    (home_id, away_id, date)
                )
                if ex:
                    continue

                try:
                    run(
                        "INSERT INTO `Match` (home_club_id,away_club_id,match_date,home_score,away_score,season,gameweek) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (home_id, away_id, date, hs, as_, season_str, gw_num)
                    )
                    season_new += 1
                    total_new += 1
                except Exception:
                    pass   # Trigger veya duplicate

        print(f"    {season_str}: {season_new} yeni mac eklendi")

    total = qone("SELECT COUNT(*) AS n FROM `Match`")["n"]
    print(f"\n  Toplam mac DB'de: {total}")

# ──────────────────────────────────────────
# BOLUM 2: PUAN DURUMLARI (maclardan hesapla)
# ──────────────────────────────────────────
def calculate_standings():
    print("\n=== PUAN DURUMLARI HESAPLANIYOR ===")
    seasons = [s for _, s in SEASONS]

    for s in seasons:
        matches = qall(
            "SELECT home_club_id, away_club_id, home_score, away_score FROM `Match` WHERE season=%s",
            (s,)
        )
        if not matches:
            continue

        stats = {}  # club_id -> {played,won,drawn,lost,gf,ga}
        for m in matches:
            for cid, gf, ga in [
                (m["home_club_id"], m["home_score"], m["away_score"]),
                (m["away_club_id"], m["away_score"], m["home_score"]),
            ]:
                if cid not in stats:
                    stats[cid] = {"played":0,"won":0,"drawn":0,"lost":0,"gf":0,"ga":0}
                d = stats[cid]
                d["played"] += 1
                d["gf"]     += gf
                d["ga"]     += ga
                if gf > ga:   d["won"]   += 1
                elif gf == ga: d["drawn"] += 1
                else:          d["lost"]  += 1

        for cid, d in stats.items():
            ex = qone("SELECT standing_id FROM LeagueStandings WHERE club_id=%s AND season=%s", (cid, s))
            if ex:
                run("""UPDATE LeagueStandings
                       SET played=%s,won=%s,drawn=%s,lost=%s,goals_for=%s,goals_against=%s
                       WHERE club_id=%s AND season=%s""",
                    (d["played"],d["won"],d["drawn"],d["lost"],d["gf"],d["ga"],cid,s))
            else:
                try:
                    run("""INSERT INTO LeagueStandings
                           (club_id,season,played,won,drawn,lost,goals_for,goals_against)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (cid,s,d["played"],d["won"],d["drawn"],d["lost"],d["gf"],d["ga"]))
                except Exception:
                    pass

        print(f"  {s}: {len(stats)} takim guncellendi")

# ──────────────────────────────────────────
# BOLUM 3: GUNCEL KADRO (football-data.org)
# ──────────────────────────────────────────
POSITION_MAP = {
    "Goalkeeper":"Goalkeeper","Centre-Back":"Defender","Left-Back":"Defender",
    "Right-Back":"Defender","Defence":"Defender","Defender":"Defender",
    "Central Midfield":"Midfielder","Defensive Midfield":"Midfielder",
    "Attacking Midfield":"Midfielder","Left Midfield":"Midfielder",
    "Right Midfield":"Midfielder","Midfield":"Midfielder","Midfielder":"Midfielder",
    "Centre-Forward":"Forward","Left Winger":"Forward","Right Winger":"Forward",
    "Attack":"Forward","Forward":"Forward","Offence":"Forward",
}

def fetch_current_squad():
    print("\n=== GUNCEL KADRO CEKILIYOR (football-data.org - 2024/25) ===")
    url = "https://api.football-data.org/v4/competitions/PL/teams"
    headers = {"X-Auth-Token": FD_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            print(f"  HATA {r.status_code}: Kadro verisi alinamadi.")
            return
        data = r.json()
    except Exception as e:
        print(f"  HATA: {e}")
        return

    added = 0
    for team in data.get("teams", []):
        club_name = team.get("shortName") or team.get("name", "")
        db_cid    = get_or_create_club(club_name)

        # Stadyum ve sehir guncelle
        if team.get("venue"):
            run("UPDATE Club SET stadium=%s WHERE club_id=%s", (team["venue"][:100], db_cid))
        if team.get("area", {}).get("name"):
            run("UPDATE Club SET city=%s WHERE club_id=%s", (team["area"]["name"], db_cid))
        if team.get("founded"):
            run("UPDATE Club SET founded=%s WHERE club_id=%s", (team["founded"], db_cid))

        for p in team.get("squad", []):
            name = p.get("name", "")
            if not name:
                continue
            parts = name.strip().split(" ", 1)
            first = parts[0]; last = parts[1] if len(parts) > 1 else ""
            pos   = POSITION_MAP.get(p.get("position",""), "Midfielder")
            dob   = (p.get("dateOfBirth") or "")[:10] or None
            nat   = p.get("nationality")
            jnum  = p.get("shirtNumber")

            ex = qone("SELECT player_id FROM Player WHERE first_name=%s AND last_name=%s", (first, last))
            if ex:
                run("UPDATE Player SET club_id=%s WHERE player_id=%s", (db_cid, ex["player_id"]))
            else:
                run("""INSERT INTO Player
                       (first_name,last_name,nationality,date_of_birth,position,jersey_number,club_id)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (first, last, nat, dob, pos, jnum, db_cid))
                added += 1

    total = qone("SELECT COUNT(*) AS n FROM Player")["n"]
    print(f"  {added} yeni oyuncu eklendi. Toplam: {total}")

# ──────────────────────────────────────────
# OZET
# ──────────────────────────────────────────
def print_summary():
    print("\n" + "="*55)
    print("  VERI TABANI OZETI")
    print("="*55)
    rows = [
        ("Club",             "Kulup"),
        ("Player",           "Oyuncu"),
        ("`Match`",          "Mac"),
        ("PlayerStatistics", "Oyuncu Istatistigi"),
        ("Transfer",         "Transfer"),
        ("Injury",           "Sakatlık"),
        ("LeagueStandings",  "Puan Durumu Kaydi"),
    ]
    for tbl, label in rows:
        n = qone(f"SELECT COUNT(*) AS n FROM {tbl}")["n"]
        print(f"  {label:25s}: {n:>6}")

    print("\n  Sezonlar:")
    for r in qall("SELECT DISTINCT season FROM LeagueStandings ORDER BY season"):
        mac_say = qone("SELECT COUNT(*) AS n FROM `Match` WHERE season=%s", (r["season"],))["n"]
        print(f"    {r['season']}  ({mac_say} mac)")

    # En cok puan alan kulup her sezon
    print("\n  Sezon Sampiyon Ozeti:")
    for _, s in SEASONS:
        row = qone("""
            SELECT c.name, (ls.won*3+ls.drawn) AS pts
            FROM LeagueStandings ls JOIN Club c ON ls.club_id=c.club_id
            WHERE ls.season=%s ORDER BY pts DESC LIMIT 1
        """, (s,))
        if row:
            print(f"    {s}: {row['name']:30s} {row['pts']} puan")

# ──────────────────────────────────────────
# ANA AKIS
# ──────────────────────────────────────────
if __name__ == "__main__":
    print("Premier League Veri Cekici v2")
    print("SE 2230 - Yasar University 2026")
    print("-" * 40)

    fetch_matches()
    calculate_standings()
    fetch_current_squad()
    print_summary()

    print("\nTamamlandi!")
