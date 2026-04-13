"""
Kaggle Transfermarkt -> premier_league_db import scripti
Sadece Premier League (GB1) verisi alinir.

KULLANIM: python import_kaggle.py
"""

import pandas as pd
import mysql.connector
import os
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────
# AYARLAR
# ──────────────────────────────────────────
KAGGLE_DIR = "kaggle_data"

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "bbb0",
    "database": "premier_league_db",
    "charset":  "utf8mb4",
}

PL_COMPETITION_ID = "GB1"  # Transfermarkt Premier League kodu

# ──────────────────────────────────────────
# DB YARDIMCILARI
# ──────────────────────────────────────────
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def qone(sql, p=()):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, p); row = cur.fetchone()
    cur.close(); conn.close(); return row

def run(sql, p=()):
    conn = get_db(); cur = conn.cursor()
    cur.execute(sql, p); conn.commit(); lid = cur.lastrowid
    cur.close(); conn.close(); return lid

def run_many(sql, params_list):
    conn = get_db(); cur = conn.cursor()
    cur.executemany(sql, params_list); conn.commit()
    cur.close(); conn.close()

def safe(val):
    """NaN -> None"""
    if pd.isna(val):
        return None
    return val

def safe_date(val):
    """Tarih formatini temizle"""
    if pd.isna(val) or val == '':
        return None
    try:
        return str(val)[:10]
    except:
        return None

def safe_int(val):
    if pd.isna(val):
        return None
    try:
        return int(float(val))
    except:
        return None

def safe_float(val):
    if pd.isna(val):
        return None
    try:
        return float(val)
    except:
        return None

# ──────────────────────────────────────────
# POZISYON MAPPING
# ──────────────────────────────────────────
POSITION_MAP = {
    "Attack":     "Forward",
    "Midfield":   "Midfielder",
    "Defender":   "Defender",
    "Goalkeeper": "Goalkeeper",
    "Centre-Forward":    "Forward",
    "Left Winger":       "Forward",
    "Right Winger":      "Forward",
    "Second Striker":    "Forward",
    "Central Midfield":  "Midfielder",
    "Attacking Midfield":"Midfielder",
    "Defensive Midfield":"Midfielder",
    "Left Midfield":     "Midfielder",
    "Right Midfield":    "Midfielder",
    "Centre-Back":       "Defender",
    "Left-Back":         "Defender",
    "Right-Back":        "Defender",
    "Sweeper":           "Defender",
    "Goalkeeper":        "Goalkeeper",
}

def map_position(pos, subpos):
    if safe(subpos) and subpos in POSITION_MAP:
        return POSITION_MAP[subpos]
    if safe(pos) and pos in POSITION_MAP:
        return POSITION_MAP[pos]
    return "Midfielder"

# ──────────────────────────────────────────
# BOLUM 1: CLUBS (PL takim bilgilerini guncelle)
# ──────────────────────────────────────────
def import_clubs():
    print("\n=== KULUP BILGILERI GUNCELLENIYOR ===")
    
    df = pd.read_csv(os.path.join(KAGGLE_DIR, "clubs.csv"))
    pl_clubs = df[df['domestic_competition_id'] == PL_COMPETITION_ID]
    
    updated = 0
    for _, row in pl_clubs.iterrows():
        name = safe(row['name'])
        if not name:
            continue
        
        stadium = safe(row['stadium_name'])
        capacity = safe_int(row['stadium_seats'])
        
        existing = qone("SELECT club_id FROM Club WHERE name = %s", (name,))
        if existing:
            if stadium:
                run("UPDATE Club SET stadium=%s WHERE name=%s", (stadium, name))
            if capacity:
                run("UPDATE Club SET capacity=%s WHERE name=%s", (capacity, name))
            updated += 1
    
    print(f"  {updated} kulup guncellendi")
    print(f"  (PL'de {len(pl_clubs)} kulup bulundu)")

# ──────────────────────────────────────────
# BOLUM 2: PLAYERS
# ──────────────────────────────────────────
def import_players():
    print("\n=== OYUNCULAR IMPORT EDILIYOR ===")
    
    df = pd.read_csv(os.path.join(KAGGLE_DIR, "players.csv"))
    
    # Sadece PL'de oynayan oyuncular
    pl_players = df[df['current_club_domestic_competition_id'] == PL_COMPETITION_ID].copy()
    
    # Tum zamanlar PL'de oynamis oyunculari da alalim (appearances'dan)
    apps = pd.read_csv(os.path.join(KAGGLE_DIR, "appearances.csv"))
    pl_apps = apps[apps['competition_id'] == PL_COMPETITION_ID]
    pl_player_ids = set(pl_apps['player_id'].unique())
    
    all_pl = df[df['player_id'].isin(pl_player_ids)].copy()
    
    print(f"  Toplam PL oyuncusu: {len(all_pl)}")
    
    # Kulup adi -> club_id eslestirmesi
    club_map = {}
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT club_id, name FROM Club")
    for r in cur.fetchall():
        club_map[r['name']] = r['club_id']
    cur.close(); conn.close()
    
    added = 0; updated = 0
    for _, row in all_pl.iterrows():
        first = safe(row['first_name']) or ''
        last  = safe(row['last_name']) or ''
        if not first and not last:
            name_parts = str(row.get('name','')).split(' ', 1)
            first = name_parts[0]
            last  = name_parts[1] if len(name_parts) > 1 else ''
        
        pos = map_position(safe(row.get('position')), safe(row.get('sub_position')))
        dob = safe_date(row.get('date_of_birth'))
        nat = safe(row.get('country_of_citizenship'))
        mv  = safe_float(row.get('market_value_in_eur'))
        mv_m = round(mv / 1_000_000, 2) if mv else None
        contract = safe_date(row.get('contract_expiration_date'))
        
        club_name = safe(row.get('current_club_name'))
        club_id = club_map.get(club_name) if club_name else None
        
        existing = qone(
            "SELECT player_id FROM Player WHERE first_name=%s AND last_name=%s",
            (first, last)
        )
        
        if existing:
            run("""UPDATE Player SET
                nationality=%s, date_of_birth=%s, position=%s,
                market_value=%s, contract_end=%s, club_id=%s
                WHERE player_id=%s""",
                (nat, dob, pos, mv_m, contract, club_id, existing['player_id']))
            updated += 1
        else:
            try:
                run("""INSERT INTO Player
                    (first_name, last_name, nationality, date_of_birth,
                     position, club_id, market_value, contract_end)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (first, last, nat, dob, pos, club_id, mv_m, contract))
                added += 1
            except Exception as e:
                pass
    
    print(f"  {added} yeni oyuncu eklendi, {updated} guncellendi")

# ──────────────────────────────────────────
# BOLUM 3: MARKET VALUES (guncel piyasa degerleri)
# ──────────────────────────────────────────
def import_market_values():
    print("\n=== PIYASA DEGERLERI GUNCELLENIYOR ===")
    
    df = pd.read_csv(os.path.join(KAGGLE_DIR, "player_valuations.csv"))
    players_df = pd.read_csv(os.path.join(KAGGLE_DIR, "players.csv"))
    
    # PL oyuncularinin en son degerlerini al
    pl_ids_df = players_df[players_df['current_club_domestic_competition_id'] == PL_COMPETITION_ID]
    pl_ids = set(pl_ids_df['player_id'].unique())
    
    pl_vals = df[df['player_id'].isin(pl_ids)].copy()
    pl_vals['date'] = pd.to_datetime(pl_vals['date'])
    
    # Her oyuncunun en son degeri
    latest = pl_vals.sort_values('date').groupby('player_id').last().reset_index()
    
    updated = 0
    for _, row in latest.iterrows():
        tm_id = int(row['player_id'])
        mv = safe_float(row.get('market_value_in_eur'))
        if not mv:
            continue
        mv_m = round(mv / 1_000_000, 2)
        
        # Transfermarkt ID ile Player'i bul - isim eslestirmesi gerekiyor
        player_row = pl_ids_df[pl_ids_df['player_id'] == tm_id]
        if player_row.empty:
            continue
        
        p = player_row.iloc[0]
        first = safe(p.get('first_name')) or ''
        last  = safe(p.get('last_name')) or ''
        
        existing = qone(
            "SELECT player_id FROM Player WHERE first_name=%s AND last_name=%s",
            (first, last)
        )
        if existing:
            run("UPDATE Player SET market_value=%s WHERE player_id=%s",
                (mv_m, existing['player_id']))
            updated += 1
    
    print(f"  {updated} oyuncunun piyasa degeri guncellendi")

# ──────────────────────────────────────────
# BOLUM 4: TRANSFERS
# ──────────────────────────────────────────
def import_transfers():
    print("\n=== TRANSFERLER IMPORT EDILIYOR ===")
    
    df = pd.read_csv(os.path.join(KAGGLE_DIR, "transfers.csv"))
    players_df = pd.read_csv(os.path.join(KAGGLE_DIR, "players.csv"))
    clubs_df = pd.read_csv(os.path.join(KAGGLE_DIR, "clubs.csv"))
    
    # PL kuluplerinin Transfermarkt ID -> DB club_id eslestirmesi
    pl_clubs_tm = clubs_df[clubs_df['domestic_competition_id'] == PL_COMPETITION_ID]
    
    # DB'deki kulup isim -> id map
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT club_id, name FROM Club")
    db_club_map = {r['name']: r['club_id'] for r in cur.fetchall()}
    cur.close(); conn.close()
    
    # TM kulup id -> DB club_id
    tm_club_to_db = {}
    for _, crow in pl_clubs_tm.iterrows():
        tm_id = int(crow['club_id'])
        name = safe(crow['name'])
        if name and name in db_club_map:
            tm_club_to_db[tm_id] = db_club_map[name]
    
    # PL ile ilgili transferler (en az bir taraf PL kulübü)
    pl_club_ids = set(pl_clubs_tm['club_id'].astype(int).tolist())
    pl_transfers = df[
        df['from_club_id'].isin(pl_club_ids) | 
        df['to_club_id'].isin(pl_club_ids)
    ].copy()
    
    print(f"  PL transferi bulundu: {len(pl_transfers)}")
    
    # Son 10 yil (2015+)
    pl_transfers['transfer_date'] = pd.to_datetime(pl_transfers['transfer_date'], errors='coerce')
    pl_transfers = pl_transfers[pl_transfers['transfer_date'].dt.year >= 2015]
    
    print(f"  2015+ PL transferi: {len(pl_transfers)}")
    
    added = 0
    for _, row in pl_transfers.iterrows():
        # Oyuncuyu bul
        player_name = safe(row.get('player_name', ''))
        if not player_name:
            continue
        
        parts = str(player_name).strip().split(' ', 1)
        first = parts[0]; last = parts[1] if len(parts) > 1 else ''
        
        player = qone(
            "SELECT player_id FROM Player WHERE first_name=%s AND last_name=%s",
            (first, last)
        )
        if not player:
            continue
        
        from_id = tm_club_to_db.get(safe_int(row.get('from_club_id')))
        to_id   = tm_club_to_db.get(safe_int(row.get('to_club_id')))
        
        if not to_id:
            continue
        
        fee = safe_float(row.get('transfer_fee'))
        fee_m = round(fee / 1_000_000, 2) if fee and fee > 0 else None
        
        date = safe_date(row.get('transfer_date'))
        season = safe(row.get('transfer_season'))
        if season:
            # "25/26" -> "2025/26" formatına çevir
            parts_s = str(season).split('/')
            if len(parts_s) == 2 and len(parts_s[0]) == 2:
                season = f"20{parts_s[0]}/{parts_s[1]}"
        
        # Zaten var mi?
        existing = qone(
            "SELECT transfer_id FROM Transfer WHERE player_id=%s AND transfer_date=%s",
            (player['player_id'], date)
        )
        if existing:
            continue
        
        try:
            run("""INSERT INTO Transfer
                (player_id, from_club_id, to_club_id, transfer_date, transfer_fee, season)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (player['player_id'], from_id, to_id, date, fee_m, season))
            added += 1
        except Exception as e:
            pass
    
    print(f"  {added} yeni transfer eklendi")

# ──────────────────────────────────────────
# OZET
# ──────────────────────────────────────────
def print_summary():
    print("\n" + "="*50)
    print("  IMPORT OZETI")
    print("="*50)
    tables = [
        ("Club", "Kulup"),
        ("Player", "Oyuncu"),
        ("`Match`", "Mac"),
        ("Transfer", "Transfer"),
        ("LeagueStandings", "Puan Durumu"),
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
    print("Kaggle Transfermarkt Import")
    print("-" * 40)
    
    # Kaggle dizini var mi?
    if not os.path.exists(KAGGLE_DIR):
        print(f"HATA: '{KAGGLE_DIR}' klasoru bulunamadi!")
        print("Once 'unzip archive.zip -d kaggle_data' calistir.")
        exit(1)
    
    import_clubs()
    import_players()
    import_market_values()
    import_transfers()
    print_summary()
    
    print("\nTamamlandi!")
