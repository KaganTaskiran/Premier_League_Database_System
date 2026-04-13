"""
Kaggle -> GameEvent + GameLineup import scripti
Sadece Premier League (GB1) maçları.

KULLANIM: python import_events.py
"""

import pandas as pd
import mysql.connector
import os
import warnings
warnings.filterwarnings('ignore')

KAGGLE_DIR = "kaggle_data"

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "bbb0",
    "database": "premier_league_db",
    "charset":  "utf8mb4",
}

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

def run_many(sql, params_list, batch=500):
    if not params_list:
        return
    conn = get_db(); cur = conn.cursor()
    for i in range(0, len(params_list), batch):
        cur.executemany(sql, params_list[i:i+batch])
        conn.commit()
    cur.close(); conn.close()

def safe(val):
    if pd.isna(val): return None
    return val

def safe_int(val):
    if pd.isna(val): return None
    try: return int(float(val))
    except: return None

# ──────────────────────────────────────────
# KAGGLE game_id -> DB match_id eslesme tablosu
# ──────────────────────────────────────────
def build_game_id_map():
    print("  Kaggle game_id <-> DB match_id eslesme tablosu olusturuluyor...")

    games = pd.read_csv(os.path.join(KAGGLE_DIR, "games.csv"))
    pl_games = games[games['competition_id'] == 'GB1'].copy()
    pl_games['date'] = pl_games['date'].astype(str).str[:10]

    clubs_df = pd.read_csv(os.path.join(KAGGLE_DIR, "clubs.csv"))
    pl_clubs = clubs_df[clubs_df['domestic_competition_id'] == 'GB1']

    # Kaggle club_id -> DB club_id
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT club_id, name FROM Club")
    db_clubs = {r['name']: r['club_id'] for r in cur.fetchall()}
    cur.close(); conn.close()

    tm_to_db_club = {}
    for _, row in pl_clubs.iterrows():
        name = safe(row['name'])
        if name and name in db_clubs:
            tm_to_db_club[int(row['club_id'])] = db_clubs[name]

    # DB match_id -> (date, home_club_id, away_club_id)
    db_matches = qall("SELECT match_id, match_date, home_club_id, away_club_id FROM `Match`")
    db_match_lookup = {}
    for m in db_matches:
        key = (str(m['match_date']), m['home_club_id'], m['away_club_id'])
        db_match_lookup[key] = m['match_id']

    game_id_map = {}  # kaggle game_id -> db match_id
    for _, row in pl_games.iterrows():
        gid = int(row['game_id'])
        date = row['date']
        home_tm = safe_int(row.get('home_club_id'))
        away_tm = safe_int(row.get('away_club_id'))
        if not home_tm or not away_tm:
            continue
        home_db = tm_to_db_club.get(home_tm)
        away_db = tm_to_db_club.get(away_tm)
        if not home_db or not away_db:
            continue
        key = (date, home_db, away_db)
        if key in db_match_lookup:
            game_id_map[gid] = db_match_lookup[key]

    print(f"  {len(game_id_map)} PL maci eslesti")
    return game_id_map

# ──────────────────────────────────────────
# BOLUM 1: GAME EVENTS
# ──────────────────────────────────────────
def import_game_events(game_id_map):
    print("\n=== MAC OLAYLARI IMPORT EDILIYOR ===")

    print("  game_events.csv okunuyor (buyuk dosya)...")
    chunks = pd.read_csv(os.path.join(KAGGLE_DIR, "game_events.csv"), chunksize=50000)

    valid_game_ids = set(game_id_map.keys())
    all_rows = []

    for chunk in chunks:
        pl_chunk = chunk[chunk['game_id'].isin(valid_game_ids)]
        all_rows.append(pl_chunk)

    if not all_rows:
        print("  Hic PL maci olayi bulunamadi.")
        return

    df = pd.concat(all_rows, ignore_index=True)
    print(f"  PL mac olayi: {len(df)}")

    # Mevcut event_id'leri al
    existing = set(r['event_id'] for r in qall("SELECT event_id FROM GameEvent"))

    params = []
    for _, row in df.iterrows():
        eid = safe(row.get('game_event_id'))
        if not eid or eid in existing:
            continue
        gid = safe_int(row.get('game_id'))
        match_id = game_id_map.get(gid)
        if not match_id:
            continue

        params.append((
            str(eid)[:50],
            match_id,
            safe_int(row.get('minute')),
            safe(row.get('type')),
            safe_int(row.get('club_id')),
            safe_int(row.get('player_id')),
            safe(row.get('description')),
            safe_int(row.get('player_in_id')),
            safe_int(row.get('player_assist_id')),
        ))

    run_many("""INSERT IGNORE INTO GameEvent
        (event_id, match_id, minute, type, club_id, player_id,
         description, player_in_id, player_assist_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", params)

    print(f"  {len(params)} mac olayi eklendi")

# ──────────────────────────────────────────
# BOLUM 2: GAME LINEUPS
# ──────────────────────────────────────────
def import_game_lineups(game_id_map):
    print("\n=== KADROLAR IMPORT EDILIYOR ===")

    print("  game_lineups.csv okunuyor (cok buyuk dosya)...")
    chunks = pd.read_csv(os.path.join(KAGGLE_DIR, "game_lineups.csv"), chunksize=50000)

    valid_game_ids = set(game_id_map.keys())
    all_rows = []

    for chunk in chunks:
        pl_chunk = chunk[chunk['game_id'].isin(valid_game_ids)]
        all_rows.append(pl_chunk)

    if not all_rows:
        print("  Hic PL kadrosu bulunamadi.")
        return

    df = pd.concat(all_rows, ignore_index=True)
    print(f"  PL kadro kaydi: {len(df)}")

    existing = set(r['lineup_id'] for r in qall("SELECT lineup_id FROM GameLineup"))

    TYPE_MAP = {
        'starting_lineup': 'starting_lineup',
        'Starting Lineup': 'starting_lineup',
        'substitutes':     'substitutes',
        'Substitutes':     'substitutes',
    }

    params = []
    for _, row in df.iterrows():
        lid = safe(row.get('game_lineups_id'))
        if not lid or lid in existing:
            continue
        gid = safe_int(row.get('game_id'))
        match_id = game_id_map.get(gid)
        if not match_id:
            continue

        ltype = TYPE_MAP.get(safe(row.get('type')), 'substitutes')

        params.append((
            str(lid)[:50],
            match_id,
            safe_int(row.get('player_id')),
            safe_int(row.get('club_id')),
            safe(row.get('player_name')),
            ltype,
            safe(row.get('position')),
            safe_int(row.get('number')),
            1 if safe_int(row.get('team_captain')) == 1 else 0,
        ))

    run_many("""INSERT IGNORE INTO GameLineup
        (lineup_id, match_id, player_id, club_id, player_name,
         type, position, number, team_captain)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", params)

    print(f"  {len(params)} kadro kaydi eklendi")

# ──────────────────────────────────────────
# OZET
# ──────────────────────────────────────────
def print_summary():
    print("\n" + "="*50)
    tables = [
        ("GameEvent",  "Mac Olayi"),
        ("GameLineup", "Kadro Kaydi"),
    ]
    for tbl, label in tables:
        conn = get_db(); cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {tbl}")
        n = cur.fetchone()[0]
        cur.close(); conn.close()
        print(f"  {label:20s}: {n:>6}")

# ──────────────────────────────────────────
# ANA AKIS
# ──────────────────────────────────────────
if __name__ == "__main__":
    print("Mac Olaylari + Kadro Import")
    print("-" * 40)

    game_id_map = build_game_id_map()

    if not game_id_map:
        print("HATA: Hic mac eslestirilemedi. Once fetch_data.py ve import_kaggle.py calistir.")
        exit(1)

    import_game_events(game_id_map)
    import_game_lineups(game_id_map)
    print_summary()

    print("\nTamamlandi!")
