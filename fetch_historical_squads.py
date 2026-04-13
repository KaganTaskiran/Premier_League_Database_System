"""
Tüm 10 Sezon (2015/16 – 2024/25) Tarihsel Kadro Çekici
- Her kulübün her sezondaki kadrosunu Transfermarkt'tan çeker
- Oyuncuları DB'ye ekler (duplicate kontrolü ile)
- Forma numarası + piyasa değeri + mevki + doğum tarihi
- Sonunda tarihsel sezonlar için PlayerStatistics üretir
"""

import requests
from bs4 import BeautifulSoup
import mysql.connector
import time, re, sys, io, unicodedata, random
from datetime import date, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB = {"host":"localhost","user":"root","password":"123456",
      "database":"premier_league_db","charset":"utf8mb4"}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
BASE = "https://www.transfermarkt.com"

# DB club_id -> (tm_slug, tm_id)
TM_MAP = {
    1:  ("fc-arsenal",               11),
    2:  ("fc-chelsea",               631),
    3:  ("fc-liverpool",             31),
    4:  ("manchester-city",          281),
    5:  ("manchester-united",        985),
    6:  ("tottenham-hotspur",        148),
    7:  ("newcastle-united",         762),
    8:  ("aston-villa",              405),
    9:  ("west-ham-united",          379),
    10: ("brighton-amp-hove-albion", 1237),
    11: ("leicester-city",           1003),
    12: ("fc-everton",               29),
    13: ("wolverhampton-wanderers",  543),
    14: ("crystal-palace",           873),
    15: ("southampton-fc",           180),
    16: ("fc-burnley",               1132),
    17: ("leeds-united",             399),
    18: ("sheffield-united",         350),
    19: ("brentford-fc",             1148),
    20: ("nottingham-forest",        703),
    21: ("fc-fulham",                931),
    22: ("west-bromwich-albion",     981),
    23: ("fc-watford",               1010),
    24: ("stoke-city",               928),
    26: ("afc-bournemouth",          989),
    29: ("sunderland-afc",           489),
    30: ("norwich-city",             97),
    32: ("swansea-city",             2290),
    36: ("hull-city",                278),
    38: ("fc-middlesbrough",         1981),
    39: ("huddersfield-town",        2448),
    40: ("cardiff-city",             157),
    58: ("luton-town",               1235),
    59: ("ipswich-town",             677),
}

# Her sezon hangi kulüpler PL'deydi (maç verisinden)
SEASON_CLUBS = {
    "2015/16": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,22,23,24,26,29,30,32,36],
    "2016/17": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,22,23,24,26,29,30,32,36,38],
    "2017/18": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,22,23,24,26,30,32,39],
    "2018/19": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,22,26,32,40],
    "2019/20": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,22,26,30],
    "2020/21": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,19,22,26,29],  # Sheffield United out
    "2021/22": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,26],
    "2022/23": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,26,30],
    "2023/24": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,26,58],
    "2024/25": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,20,21,26,59],
}

# Sezon -> TM saison_id
SEASON_TM_ID = {
    "2015/16": 2015, "2016/17": 2016, "2017/18": 2017,
    "2018/19": 2018, "2019/20": 2019, "2020/21": 2020,
    "2021/22": 2021, "2022/23": 2022, "2023/24": 2023, "2024/25": 2024,
}

POS_MAP = {
    "Goalkeeper": "Goalkeeper",
    "Centre-Back": "Defender", "Left-Back": "Defender", "Right-Back": "Defender",
    "Defensive Midfield": "Midfielder", "Central Midfield": "Midfielder",
    "Attacking Midfield": "Midfielder", "Left Midfield": "Midfielder",
    "Right Midfield": "Midfielder",
    "Left Winger": "Forward", "Right Winger": "Forward",
    "Second Striker": "Forward", "Centre-Forward": "Forward",
}

def dbconn():
    return mysql.connector.connect(**DB)

def qall(sql, p=()):
    c = dbconn(); cur = c.cursor(dictionary=True)
    cur.execute(sql, p); r = cur.fetchall(); cur.close(); c.close(); return r

def qone(sql, p=()):
    r = qall(sql, p); return r[0] if r else None

def run(sql, p=()):
    c = dbconn(); cur = c.cursor()
    cur.execute(sql, p); c.commit(); lid = cur.lastrowid; cur.close(); c.close(); return lid

def runmany(sql, data):
    c = dbconn(); cur = c.cursor()
    cur.executemany(sql, data); c.commit(); n = cur.rowcount; cur.close(); c.close(); return n

def normalize(name):
    n = unicodedata.normalize("NFD", name)
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", n.lower())).strip()

def parse_value(s):
    s = s.strip().replace("\xa0","").lower().replace("€","").replace(",",".")
    if not s or s in ["-","n/a",""]: return None
    try:
        if "m" in s: return round(float(s.replace("m","")), 2)
        if "k" in s: return round(float(s.replace("k","")) / 1000, 3)
    except: pass
    return None

def split_name(full):
    parts = full.strip().split()
    if len(parts) == 1: return "", parts[0]
    return parts[0], " ".join(parts[1:])

def get_page(url, delay=1.5):
    time.sleep(delay)
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def scrape_squad(slug, tm_id, saison_id):
    url = f"{BASE}/{slug}/startseite/verein/{tm_id}/saison_id/{saison_id}"
    soup = get_page(url)
    players = []
    for row in soup.select("table.items tbody tr"):
        num_td  = row.select_one("td.rueckennummer")
        name_td = row.select_one("td.hauptlink a[href*='/profil/spieler/']")
        if not name_td: continue

        name = name_td.text.strip()
        try: jersey = int(num_td.text.strip()) if num_td else None
        except: jersey = None

        pos_text = ""
        for td in row.select("td"):
            if td.text.strip() in POS_MAP:
                pos_text = td.text.strip(); break
        position = POS_MAP.get(pos_text, "Midfielder")

        flag = row.select_one("img.flaggenrahmen")
        nationality = flag["title"] if flag and flag.get("title") else None

        dob = None
        age_td = row.select_one("td.zentriert[title]")
        if age_td and age_td.get("title"):
            m = re.search(r"(\w+ \d+, \d{4})", age_td["title"])
            if m:
                try: dob = datetime.strptime(m.group(1), "%b %d, %Y").date()
                except: pass

        val_tds = row.select("td.rechts")
        val = None
        for vtd in reversed(val_tds):
            v = parse_value(vtd.text)
            if v: val = v; break

        players.append({"name": name, "jersey": jersey, "position": position,
                         "nationality": nationality, "dob": dob, "value": val})
    return players


# Global cache: normalize(name) -> player_id
_player_cache = {}

def build_cache():
    global _player_cache
    rows = qall("SELECT player_id, first_name, last_name FROM Player")
    _player_cache = {}
    for p in rows:
        fn = (p["first_name"] or "").strip()
        ln = (p["last_name"] or "").strip()
        key = normalize(f"{fn} {ln}")
        _player_cache[key] = p["player_id"]
        # last name alone
        lkey = normalize(ln)
        if lkey and lkey not in _player_cache:
            _player_cache[lkey] = p["player_id"]

def find_or_create_player(p_info, club_id):
    """Oyuncuyu cache'te ara, yoksa oluştur. player_id döndür."""
    name = p_info["name"]
    norm = normalize(name)
    parts = norm.split()
    last  = parts[-1] if parts else ""

    # Tam isim eşleşmesi
    if norm in _player_cache:
        return _player_cache[norm]
    # Soyisim eşleşmesi
    if last in _player_cache:
        return _player_cache[last]

    # Yeni oyuncu ekle
    fn, ln = split_name(name)
    try:
        pid = run("""INSERT INTO Player
            (first_name, last_name, nationality, date_of_birth, position,
             jersey_number, club_id, market_value)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (fn, ln, p_info["nationality"], p_info["dob"],
             p_info["position"], p_info["jersey"], club_id, p_info["value"]))
        # Cache'e ekle
        _player_cache[norm] = pid
        if last not in _player_cache:
            _player_cache[last] = pid
        return pid
    except:
        return None


def generate_historical_stats():
    """2015/16 – 2023/24 maçları için PlayerStatistics üret"""
    print("\n=== TARIHI SEZON ISTATISTIKLERI OLUSTURULUYOR ===")

    seasons = [s for s in SEASON_TM_ID.keys() if s != "2024/25"]
    existing = set()
    ex_rows = qall("SELECT match_id, player_id FROM PlayerStatistics")
    for r in ex_rows:
        existing.add((r["match_id"], r["player_id"]))

    club_players = {}
    all_pl = qall("SELECT player_id, club_id, position FROM Player")
    for p in all_pl:
        cid = p["club_id"]; pos = p["position"] or "Midfielder"
        club_players.setdefault(cid, {}).setdefault(pos, []).append(p["player_id"])

    random.seed(42)
    batch = []
    total_matches = 0

    for season in seasons:
        matches = qall(
            "SELECT match_id, home_club_id, away_club_id, home_score, away_score "
            "FROM `Match` WHERE season=%s ORDER BY match_id", (season,))
        total_matches += len(matches)

        for m in matches:
            mid = m["match_id"]
            for cid, goals in [(m["home_club_id"], m["home_score"]),
                               (m["away_club_id"], m["away_score"])]:
                if cid not in club_players: continue
                fwd  = club_players[cid].get("Forward", [])
                mid_p= club_players[cid].get("Midfielder", [])
                dfd  = club_players[cid].get("Defender", [])
                gkp  = club_players[cid].get("Goalkeeper", [])
                if not (fwd or mid_p): continue

                # 11 kadro + 3 yedek
                squad = []
                if gkp: squad += random.sample(gkp, min(1, len(gkp)))
                if dfd:  squad += random.sample(dfd,  min(4, len(dfd)))
                if mid_p:squad += random.sample(mid_p,min(4, len(mid_p)))
                if fwd:  squad += random.sample(fwd,  min(3, len(fwd)))
                extras = [p for p in (fwd+mid_p+dfd+gkp) if p not in squad]
                squad += random.sample(extras, min(3, len(extras)))

                # Gol dağıtımı
                pool = fwd * 3 + mid_p
                scorers = {}
                for _ in range(goals):
                    if pool:
                        s = random.choice(pool)
                        scorers[s] = scorers.get(s, 0) + 1

                # Asist
                assisters = {}
                a_pool = fwd + mid_p * 2 + dfd
                for _ in range(sum(scorers.values())):
                    if a_pool and random.random() < 0.70:
                        a = random.choice(a_pool)
                        assisters[a] = assisters.get(a, 0) + 1

                yc_players = random.sample(squad, min(random.randint(0,2), len(squad)))
                rc_player  = random.choice(squad) if random.random() < 0.04 else None

                for pid in squad:
                    if (mid, pid) in existing: continue
                    g  = scorers.get(pid, 0)
                    a  = assisters.get(pid, 0)
                    yc = 1 if pid in yc_players else 0
                    rc = 1 if pid == rc_player  else 0
                    mins = 90 if pid == (gkp[0] if gkp else -1) else \
                           random.randint(60,90) if pid in squad[:11] else \
                           random.randint(15,45)
                    sot = g + (random.randint(0,2) if pid in fwd+mid_p else 0)
                    batch.append((pid, mid, g, a, yc, rc, mins, sot))
                    existing.add((mid, pid))

    if batch:
        inserted = runmany("""
            INSERT IGNORE INTO PlayerStatistics
            (player_id,match_id,goals,assists,yellow_cards,red_cards,minutes_played,shots_on_target)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, batch)
        print(f"  {inserted} istatistik kaydı eklendi ({total_matches} maç için)")
    else:
        print("  Eklenecek istatistik bulunamadı")


def main():
    print("=" * 60)
    print("  10 SEZON TARIHI KADRO CEKICI  (2015/16 – 2024/25)")
    print("=" * 60)

    build_cache()
    print(f"  Mevcut oyuncu cache: {len(_player_cache)} kayıt\n")

    total_new = 0
    processed = 0
    errors    = 0

    seasons = list(SEASON_TM_ID.keys())

    for season in seasons:
        clubs = SEASON_CLUBS.get(season, [])
        saison_id = SEASON_TM_ID[season]
        print(f"\n--- {season} ({len(clubs)} kulüp) ---")

        for club_id in clubs:
            if club_id not in TM_MAP:
                continue
            slug, tm_id = TM_MAP[club_id]
            club_name = qone("SELECT name FROM Club WHERE club_id=%s", (club_id,))
            cname = club_name["name"] if club_name else f"club_{club_id}"

            try:
                squad = scrape_squad(slug, tm_id, saison_id)
                new_count = 0
                for p_info in squad:
                    pid = find_or_create_player(p_info, club_id)
                    if pid and pid > 803:  # yeni eklenen
                        new_count += 1

                total_new += new_count
                processed += 1
                print(f"  {cname:<35} {len(squad):3} oyuncu, {new_count:3} yeni")

            except Exception as e:
                errors += 1
                print(f"  {cname:<35} HATA: {e}")

    print(f"\n{'='*60}")
    print(f"  İşlenen: {processed}, Yeni oyuncu: {total_new}, Hata: {errors}")

    total_players = qone("SELECT COUNT(*) AS n FROM Player")["n"]
    print(f"  Toplam oyuncu: {total_players}")

    # Tarihsel istatistikler
    generate_historical_stats()

    # Final özet
    r = qone("""SELECT COUNT(*) AS t, COUNT(jersey_number) AS jn,
                       COUNT(market_value) AS mv FROM Player""")
    ps = qone("SELECT COUNT(*) AS n FROM PlayerStatistics")
    print(f"\n  FINAL DURUM:")
    print(f"  Oyuncu         : {r['t']}")
    print(f"  Forma numarası : {r['jn']}")
    print(f"  Piyasa değeri  : {r['mv']}")
    print(f"  Oyuncu stat.   : {ps['n']}")
    print("\nTamamlandı!")


if __name__ == "__main__":
    main()
