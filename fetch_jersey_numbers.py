"""
Transfermarkt Jersey Number Scraper
- 20 Premier League takımının 2024/25 kadrosundaki forma numaralarını çeker
- DB'deki oyuncularla isim eşleştirmesi yaparak günceller
"""

import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
import re
import sys
import io
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB = {"host":"localhost","user":"root","password":"123456",
      "database":"premier_league_db","charset":"utf8mb4"}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
BASE = "https://www.transfermarkt.com"

# TM URL -> DB club_id eşlemesi
TEAM_MAP = [
    ("/manchester-city/startseite/verein/281/saison_id/2024",      4),
    ("/fc-chelsea/startseite/verein/631/saison_id/2024",           2),
    ("/fc-arsenal/startseite/verein/11/saison_id/2024",            1),
    ("/fc-liverpool/startseite/verein/31/saison_id/2024",          3),
    ("/manchester-united/startseite/verein/985/saison_id/2024",    5),
    ("/tottenham-hotspur/startseite/verein/148/saison_id/2024",    6),
    ("/aston-villa/startseite/verein/405/saison_id/2024",          8),
    ("/newcastle-united/startseite/verein/762/saison_id/2024",     7),
    ("/brighton-amp-hove-albion/startseite/verein/1237/saison_id/2024", 10),
    ("/crystal-palace/startseite/verein/873/saison_id/2024",       14),
    ("/afc-bournemouth/startseite/verein/989/saison_id/2024",      26),
    ("/nottingham-forest/startseite/verein/703/saison_id/2024",    20),
    ("/wolverhampton-wanderers/startseite/verein/543/saison_id/2024", 13),
    ("/brentford-fc/startseite/verein/1148/saison_id/2024",        19),
    ("/west-ham-united/startseite/verein/379/saison_id/2024",      9),
    ("/fc-everton/startseite/verein/29/saison_id/2024",            12),
    ("/fc-fulham/startseite/verein/931/saison_id/2024",            21),
    ("/southampton-fc/startseite/verein/180/saison_id/2024",       15),
    ("/ipswich-town/startseite/verein/677/saison_id/2024",         59),
    ("/leicester-city/startseite/verein/1003/saison_id/2024",      11),
]

def get_page(url):
    time.sleep(2)
    r = requests.get(BASE + url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def db_conn():
    return mysql.connector.connect(**DB)

def qall(sql, p=()):
    c = db_conn(); cur = c.cursor(dictionary=True)
    cur.execute(sql, p); r = cur.fetchall(); cur.close(); c.close(); return r

def run(sql, p=()):
    c = db_conn(); cur = c.cursor()
    cur.execute(sql, p); c.commit(); cur.close(); c.close()

def normalize(name):
    n = unicodedata.normalize("NFD", name)
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    n = re.sub(r"[^a-z0-9 ]", "", n.lower())
    return re.sub(r"\s+", " ", n).strip()

def scrape_squad(url_path):
    """Returns list of (full_name, jersey_number)"""
    soup = get_page(url_path)
    players = []
    rows = soup.select("table.items tbody tr")
    for row in rows:
        num_td  = row.select_one("td.rueckennummer")
        name_td = row.select_one("td.hauptlink a[href*='/profil/spieler/']")
        if not num_td or not name_td:
            continue
        name = name_td.text.strip()
        try:
            jersey = int(num_td.text.strip())
        except ValueError:
            jersey = None
        if name and jersey:
            players.append((name, jersey))
    return players

def update_jerseys(club_id, squad):
    """squad: [(name, jersey), ...], eşleştirip günceller"""
    db_players = qall(
        "SELECT player_id, first_name, last_name FROM Player WHERE club_id=%s",
        (club_id,)
    )

    # DB lookup: normalize(fullname) -> player_id
    lookup_full = {}
    lookup_last = {}
    for p in db_players:
        fn = (p["first_name"] or "").strip()
        ln = (p["last_name"] or "").strip()
        full_n = normalize(f"{fn} {ln}")
        last_n = normalize(ln)
        lookup_full[full_n] = p["player_id"]
        lookup_last.setdefault(last_n, []).append(p["player_id"])

    updated = 0
    used_jerseys = set()

    for tm_name, jersey in squad:
        if jersey in used_jerseys:
            continue
        norm = normalize(tm_name)
        parts = norm.split()
        last  = parts[-1] if parts else ""

        pid = None
        if norm in lookup_full:
            pid = lookup_full[norm]
        elif last in lookup_last and len(lookup_last[last]) == 1:
            pid = lookup_last[last][0]
        # Partial: first token of TM name vs last name
        if not pid and parts:
            first_tok = parts[0]
            candidates = [v[0] for k, v in lookup_last.items()
                          if first_tok in k and len(v) == 1]
            if len(candidates) == 1:
                pid = candidates[0]

        if pid:
            run("UPDATE Player SET jersey_number=%s WHERE player_id=%s AND (jersey_number IS NULL OR jersey_number != %s)",
                (jersey, pid, jersey))
            used_jerseys.add(jersey)
            updated += 1

    return updated


def main():
    print("=" * 55)
    print("  TRANSFERMARKT FORMA NUMARASI CEKICI")
    print("=" * 55)

    total_updated = 0

    for i, (url_path, club_id) in enumerate(TEAM_MAP, 1):
        club = qall("SELECT name FROM Club WHERE club_id=%s", (club_id,))
        club_name = club[0]["name"] if club else f"club_id={club_id}"
        try:
            squad = scrape_squad(url_path)
            updated = update_jerseys(club_id, squad)
            print(f"  [{i:2}/20] {club_name:<35} {len(squad):3} oyuncu cekildi, {updated:3} guncellendi")
            total_updated += updated
        except Exception as e:
            print(f"  [{i:2}/20] {club_name:<35} HATA: {e}")

    print(f"\n  Toplam guncellenen: {total_updated} oyuncu")

    # Sonuç istatistikleri
    r = qall("SELECT COUNT(*) AS t, COUNT(jersey_number) AS has_num FROM Player")[0]
    print(f"\n  Forma numarasi olan: {r['has_num']} / {r['t']}")

    # Kontrol: Arsenal kadrosu
    print("\n  Arsenal 2024/25 Kadrosu (forma sirasina gore):")
    players = qall("""
        SELECT jersey_number, CONCAT(first_name,' ',last_name) AS oyuncu, position
        FROM Player WHERE club_id=1 AND jersey_number IS NOT NULL
        ORDER BY jersey_number
    """)
    for p in players:
        print(f"    #{p['jersey_number']:<3} {p['oyuncu']:<30} {p['position']}")

    print("\nTamamlandi!")


if __name__ == "__main__":
    main()
