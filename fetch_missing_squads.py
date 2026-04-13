"""
Southampton, Ipswich Town ve Leicester City kadrosunu Transfermarkt'tan çekip DB'ye ekler.
Ayrıca forma numarası hâlâ NULL olan oyunculara akıllı atama yapar.
"""
import requests
from bs4 import BeautifulSoup
import mysql.connector
import time, re, sys, io, unicodedata
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB = {"host":"localhost","user":"root","password":"123456",
      "database":"premier_league_db","charset":"utf8mb4"}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
BASE = "https://www.transfermarkt.com"

MISSING_CLUBS = [
    (15,  "Southampton",  "/southampton-fc/startseite/verein/180/saison_id/2024"),
    (59,  "Ipswich Town", "/ipswich-town/startseite/verein/677/saison_id/2024"),
    (11,  "Leicester City","/leicester-city/startseite/verein/1003/saison_id/2024"),
]

def dbconn(): return mysql.connector.connect(**DB)
def qall(sql,p=()):
    c=dbconn();cur=c.cursor(dictionary=True);cur.execute(sql,p);r=cur.fetchall();cur.close();c.close();return r
def qone(sql,p=()):
    r=qall(sql,p);return r[0] if r else None
def run(sql,p=()):
    c=dbconn();cur=c.cursor();cur.execute(sql,p);c.commit();lid=cur.lastrowid;cur.close();c.close();return lid

def normalize(n):
    n = unicodedata.normalize("NFD", n)
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]","",n.lower())).strip()

def parse_value(s):
    s = s.strip().replace("\xa0","").lower().replace("€","").replace(",",".")
    if not s or s in ["-","n/a",""]: return None
    try:
        if "m" in s: return round(float(s.replace("m","")),2)
        if "k" in s: return round(float(s.replace("k",""))/1000,3)
    except: pass
    return None

def get_page(path):
    time.sleep(2)
    r = requests.get(BASE+path, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text,"html.parser")

def scrape_full_squad(path):
    """Returns list of dicts: name, jersey, position, nationality, dob, value"""
    soup = get_page(path)
    players = []
    rows = soup.select("table.items tbody tr")

    for row in rows:
        num_td  = row.select_one("td.rueckennummer")
        name_td = row.select_one("td.hauptlink a[href*='/profil/spieler/']")
        if not name_td or not num_td: continue

        name = name_td.text.strip()
        try: jersey = int(num_td.text.strip())
        except: jersey = None

        # Position
        pos_td = row.select_one("td[title]") or row.find("td", string=re.compile(r"Goalkeeper|Defender|Midfielder|Forward|Winger|Striker|Back|Centre"))
        position = None
        pos_text = ""
        for td in row.select("td"):
            t = td.text.strip()
            if t in ("Goalkeeper","Centre-Back","Left-Back","Right-Back",
                     "Defensive Midfield","Central Midfield","Attacking Midfield",
                     "Left Midfield","Right Midfield","Left Winger","Right Winger",
                     "Second Striker","Centre-Forward"):
                pos_text = t; break

        POS_MAP = {
            "Goalkeeper": "Goalkeeper",
            "Centre-Back": "Defender", "Left-Back": "Defender", "Right-Back": "Defender",
            "Defensive Midfield": "Midfielder", "Central Midfield": "Midfielder",
            "Attacking Midfield": "Midfielder", "Left Midfield": "Midfielder",
            "Right Midfield": "Midfielder",
            "Left Winger": "Forward", "Right Winger": "Forward",
            "Second Striker": "Forward", "Centre-Forward": "Forward",
        }
        position = POS_MAP.get(pos_text, "Midfielder")

        # Nationality - flag img alt
        flag = row.select_one("img.flaggenrahmen")
        nationality = flag["title"] if flag and flag.get("title") else None

        # DoB (age column)
        age_td = row.select_one("td.zentriert[title]")
        dob = None
        if age_td and age_td.get("title"):
            m = re.search(r"(\w+ \d+, \d{4})", age_td["title"])
            if m:
                try:
                    from datetime import datetime
                    dob = datetime.strptime(m.group(1), "%b %d, %Y").date()
                except: pass

        # Market value
        val_tds = row.select("td.rechts")
        val = None
        for vtd in reversed(val_tds):
            v = parse_value(vtd.text)
            if v: val = v; break

        players.append({
            "name": name, "jersey": jersey, "position": position,
            "nationality": nationality, "dob": dob, "value": val,
        })
    return players

def split_name(full):
    """'Armel Bella-Kotchap' -> first='Armel', last='Bella-Kotchap'"""
    parts = full.strip().split()
    if len(parts) == 1: return "", parts[0]
    return parts[0], " ".join(parts[1:])

def add_squad(club_id, squad):
    existing = qall("SELECT player_id, first_name, last_name FROM Player WHERE club_id=%s", (club_id,))
    exist_norms = {normalize(f"{p['first_name']} {p['last_name']}"): p["player_id"] for p in existing}

    added = 0
    for p in squad:
        norm = normalize(p["name"])
        if norm in exist_norms:
            # Sadece jersey ve değer güncelle
            pid = exist_norms[norm]
            if p["jersey"]:
                run("UPDATE Player SET jersey_number=%s WHERE player_id=%s AND jersey_number IS NULL", (p["jersey"], pid))
            if p["value"]:
                run("UPDATE Player SET market_value=%s WHERE player_id=%s AND market_value IS NULL", (p["value"], pid))
            continue

        fn, ln = split_name(p["name"])
        try:
            run("""INSERT INTO Player
                (first_name, last_name, nationality, date_of_birth, position,
                 jersey_number, club_id, market_value)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (fn, ln, p["nationality"], p["dob"], p["position"],
                 p["jersey"], club_id, p["value"]))
            added += 1
        except Exception as e:
            pass
    return added


def fill_null_jerseys():
    """Hâlâ NULL olan jersey_number'ları kulüp içinde boş numaralarla doldur"""
    print("\n=== NULL FORMA NUMARALARI DOLDURULUYOR ===")
    clubs = qall("SELECT DISTINCT club_id FROM Player WHERE jersey_number IS NULL")
    total = 0
    for c in clubs:
        cid = c["club_id"]
        # Bu kulüpte kullanılan numaralar
        used = {r["jersey_number"] for r in qall(
            "SELECT jersey_number FROM Player WHERE club_id=%s AND jersey_number IS NOT NULL", (cid,))}
        # NULL oyuncular
        nulls = qall("SELECT player_id, position FROM Player WHERE club_id=%s AND jersey_number IS NULL", (cid,))

        # Önce pozisyona göre tipik aralıktan boş numara bul
        POS_RANGES = {
            "Goalkeeper":  list(range(1, 5)),
            "Defender":    list(range(2, 25)),
            "Midfielder":  list(range(6, 35)),
            "Forward":     list(range(7, 40)),
        }
        all_available = [n for n in range(1, 100) if n not in used]

        for p in nulls:
            pos = p["position"] or "Midfielder"
            preferred = [n for n in POS_RANGES.get(pos, range(1,99)) if n not in used]
            if preferred:
                num = preferred[0]
            elif all_available:
                num = all_available[0]
            else:
                break
            run("UPDATE Player SET jersey_number=%s WHERE player_id=%s", (num, p["player_id"]))
            used.add(num)
            if num in all_available: all_available.remove(num)
            total += 1
    print(f"  {total} oyuncuya forma numarası atandı")


def main():
    print("=" * 55)
    print("  EKSIK KADRO + FORMA NUMARASI TAMAMLAYICI")
    print("=" * 55)

    # 1. Eksik kulüplerin kadrosunu çek ve ekle
    print("\n=== EKSIK KULUP KADROLARI ===")
    for club_id, club_name, path in MISSING_CLUBS:
        try:
            squad = scrape_full_squad(path)
            added = add_squad(club_id, squad)
            total_now = qone("SELECT COUNT(*) AS n FROM Player WHERE club_id=%s", (club_id,))["n"]
            print(f"  {club_name:<20}: {len(squad)} TM oyuncu, {added} yeni eklendi, toplam: {total_now}")
        except Exception as e:
            print(f"  {club_name}: HATA -> {e}")

    # 2. Hâlâ NULL olan jersey'leri doldur
    fill_null_jerseys()

    # Final özet
    r = qone("SELECT COUNT(*) AS t, COUNT(jersey_number) AS jn FROM Player")
    print(f"\n  SONUC: {r['jn']} / {r['t']} oyuncunun forma numarası var")

    # Arsenal kontrol
    print("\n  Arsenal Kadrosu (forma #'ya göre):")
    ars = qall("""SELECT jersey_number, CONCAT(first_name,' ',last_name) AS n, position
                  FROM Player WHERE club_id=1 AND jersey_number IS NOT NULL
                  ORDER BY jersey_number LIMIT 20""")
    for p in ars:
        print(f"    #{p['jersey_number']:<3} {p['n']:<28} {p['position']}")

    print("\nTamamlandi!")

if __name__ == "__main__":
    main()
