"""
Market Value Assignment Script
- Bilinen yildizlara gercek Transfermarkt degerleri (2024/25 Ocak donemi)
- Geri kalan oyunculara pozisyon/yas/kulup tier bazli gercekci degerler
"""
import mysql.connector, random, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB = {"host":"localhost","user":"root","password":"123456",
      "database":"premier_league_db","charset":"utf8mb4"}

def conn(): return mysql.connector.connect(**DB)
def qall(sql,p=()):
    c=conn();cur=c.cursor(dictionary=True);cur.execute(sql,p);r=cur.fetchall();cur.close();c.close();return r
def qone(sql,p=()):
    r=qall(sql,p);return r[0] if r else None
def run(sql,p=()):
    c=conn();cur=c.cursor();cur.execute(sql,p);c.commit();cur.close();c.close()

# ── Gercek Transfermarkt degerleri (milyon €, Ocak 2025) ──────────────────────
REAL_VALUES = {
    # Arsenal
    "Bukayo Saka":          150,
    "Martin Odegaard":      120,
    "Declan Rice":          100,
    "Kai Havertz":           80,
    "Gabriel Magalhaes":     80,
    "David Raya":            35,
    "Gabriel Martinelli":    70,
    "Leandro Trossard":      40,
    "Ben White":             70,
    "Mikel Merino":          50,
    "Viktor Gyokeres":       90,
    "Noni Madueke":          50,

    # Chelsea
    "Cole Palmer":          150,
    "Nicolas Jackson":       70,
    "Enzo Fernandez":        80,
    "Moises Caicedo":        80,
    "Reece James":           50,
    "Levi Colwill":          60,
    "Marc Cucurella":        35,
    "Pedro Neto":            65,
    "Christopher Nkunku":    70,

    # Liverpool
    "Mohamed Salah":        100,
    "Virgil van Dijk":       50,
    "Trent Alexander-Arnold":70,
    "Alisson Becker":        45,
    "Alexis Mac Allister":   70,
    "Dominik Szoboszlai":    70,
    "Luis Diaz":             80,
    "Darwin Nunez":          75,
    "Cody Gakpo":            60,
    "Ryan Gravenberch":      65,
    "Ibrahima Konate":       60,
    "Andrew Robertson":      35,

    # Manchester City
    "Erling Haaland":       180,
    "Phil Foden":           150,
    "Kevin De Bruyne":       60,
    "Rodri":                 120,
    "Bernardo Silva":         70,
    "Jack Grealish":          55,
    "Ruben Dias":             70,
    "Ederson":                40,
    "Josko Gvardiol":         90,
    "Jeremy Doku":            70,
    "Manuel Akanji":          50,
    "Matheus Nunes":          50,

    # Manchester United
    "Bruno Fernandes":        70,
    "Marcus Rashford":        45,
    "Rasmus Hojlund":         60,
    "Kobbie Mainoo":          80,
    "Alejandro Garnacho":     65,
    "Andre Onana":            35,
    "Lisandro Martinez":      65,
    "Harry Maguire":          25,

    # Newcastle
    "Alexander Isak":        110,
    "Bruno Guimaraes":        90,
    "Anthony Gordon":         70,
    "Kieran Trippier":        25,
    "Sandro Tonali":          55,
    "Harvey Barnes":          40,

    # Aston Villa
    "Ollie Watkins":          75,
    "Emiliano Martinez":      35,
    "Leon Bailey":            35,
    "Youri Tielemans":        35,
    "Douglas Luiz":           50,
    "Morgan Rogers":          45,
    "Boubacar Kamara":        40,
    "Amadou Onana":           50,

    # Tottenham
    "Son Heung-min":          40,
    "James Maddison":         55,
    "Dejan Kulusevski":       55,
    "Richarlison":            40,
    "Cristian Romero":        70,
    "Pape Matar Sarr":        55,
    "Dominic Solanke":        40,
    "Brennan Johnson":        50,

    # Brighton
    "Kaoru Mitoma":           60,
    "Evan Ferguson":          50,
    "Joao Pedro":             50,
    "Mats Wieffer":           40,
    "Adam Webster":           20,

    # Wolves
    "Pedro Neto":             65,
    "Matheus Cunha":          55,
    "Hwang Hee-chan":         30,
    "Joao Gomes":             40,

    # West Ham
    "Mohammed Kudus":         60,
    "Lucas Paqueta":          55,
    "Jarrod Bowen":           60,
    "Edson Alvarez":          40,

    # Crystal Palace
    "Eberechi Eze":           70,
    "Michael Olise":          60,
    "Jean-Philippe Mateta":   40,
    "Marc Guehi":             55,

    # Everton
    "Jarrad Branthwaite":     70,
    "Dominic Calvert-Lewin":  25,
    "Idrissa Gueye":          15,
    "Abdoulaye Doucoure":     20,

    # Fulham
    "Raul Jimenez":           18,
    "Andreas Pereira":        30,
    "Joao Palhinha":          55,
    "Rodrigo Muniz":          30,
    "Adama Traore":           20,

    # Brentford
    "Bryan Mbeumo":           55,
    "Yoane Wissa":            40,
    "Christian Norgaard":     25,
    "Keane Lewis-Potter":     25,
    "Ivan Toney":             50,

    # Nottingham Forest
    "Callum Hudson-Odoi":     30,
    "Morgan Gibbs-White":     50,
    "Chris Wood":             15,
    "Anthony Elanga":         40,
    "Elliot Anderson":        35,

    # Leicester
    "Jamie Vardy":            10,
    "Kiernan Dewsbury-Hall":  35,
    "Stephy Mavididi":        25,

    # Southampton
    "Tyler Dibling":          30,
    "Adam Armstrong":         15,

    # Bournemouth
    "Dominic Solanke":        40,
    "Antoine Semenyo":        30,
    "Philip Billing":         20,

    # Ipswich
    "Liam Delap":             35,
    "Omari Hutchinson":       30,
}

# ── Kulup tier (2024/25 puanina gore) ─────────────────────────────────────────
CLUB_TIER = {
    3:  "elite",   # Liverpool   84pts
    1:  "elite",   # Arsenal     74pts
    4:  "elite",   # Man City    71pts
    2:  "elite",   # Chelsea     69pts
    7:  "top",     # Newcastle   66pts
    8:  "top",     # Aston Villa 66pts
    20: "top",     # Nott Forest 65pts
    10: "top",     # Brighton    61pts
    19: "mid",     # Brentford   56pts
    26: "mid",     # Bournemouth 56pts
    21: "mid",     # Fulham      54pts
    14: "mid",     # Crystal Pal 53pts
    12: "mid",     # Everton     48pts
    9:  "lower",   # West Ham    43pts
    5:  "lower",   # Man United  42pts
    13: "lower",   # Wolves      42pts
    6:  "lower",   # Tottenham   38pts
    11: "bottom",  # Leicester   25pts
    59: "bottom",  # Ipswich     22pts
    15: "bottom",  # Southampton 12pts
}

# Pozisyon x tier -> (min, max) piyasa degeri M€
VALUE_RANGE = {
    ("Forward",    "elite"):  (25, 90),
    ("Forward",    "top"):    (15, 60),
    ("Forward",    "mid"):    (8,  40),
    ("Forward",    "lower"):  (5,  30),
    ("Forward",    "bottom"): (3,  20),
    ("Midfielder", "elite"):  (20, 80),
    ("Midfielder", "top"):    (12, 55),
    ("Midfielder", "mid"):    (7,  35),
    ("Midfielder", "lower"):  (5,  28),
    ("Midfielder", "bottom"): (3,  18),
    ("Defender",   "elite"):  (15, 70),
    ("Defender",   "top"):    (10, 45),
    ("Defender",   "mid"):    (6,  30),
    ("Defender",   "lower"):  (4,  22),
    ("Defender",   "bottom"): (2,  15),
    ("Goalkeeper", "elite"):  (15, 45),
    ("Goalkeeper", "top"):    (8,  30),
    ("Goalkeeper", "mid"):    (4,  20),
    ("Goalkeeper", "lower"):  (3,  15),
    ("Goalkeeper", "bottom"): (2,  10),
}

def age_factor(dob):
    """Yas carpani: 24-28 arasi zirvede"""
    if not dob:
        return 1.0
    from datetime import date
    age = (date.today() - dob).days // 365
    if age < 20:   return 0.65
    if age < 23:   return 0.85
    if age < 26:   return 1.10
    if age < 29:   return 1.0
    if age < 32:   return 0.75
    return 0.45

def main():
    random.seed(2025)

    print("=== PIYASA DEGERLERI ATANIYOR ===\n")

    players = qall("""
        SELECT player_id, first_name, last_name, position, club_id, date_of_birth, market_value
        FROM Player
    """)

    # Gercek deger atamalari
    real_count = 0
    for p in players:
        full = f"{p['first_name']} {p['last_name']}".strip()
        # Tam isim eşleşmesi
        if full in REAL_VALUES:
            v = REAL_VALUES[full]
            run("UPDATE Player SET market_value=%s WHERE player_id=%s", (v, p["player_id"]))
            real_count += 1
            continue
        # Soyisim eşleşmesi (benzersizse)
        ln = p["last_name"] or ""
        matches = [k for k in REAL_VALUES if k.split()[-1].lower() == ln.lower()]
        if len(matches) == 1:
            v = REAL_VALUES[matches[0]]
            run("UPDATE Player SET market_value=%s WHERE player_id=%s", (v, p["player_id"]))
            real_count += 1

    print(f"  Gercek deger atanan oyuncu: {real_count}")

    # Kalan NULL oyuncular icin tahmin
    nulls = qall("SELECT player_id, position, club_id, date_of_birth FROM Player WHERE market_value IS NULL")
    gen_count = 0
    for p in nulls:
        pos   = p["position"] or "Midfielder"
        tier  = CLUB_TIER.get(p["club_id"], "mid")
        key   = (pos, tier)
        lo, hi = VALUE_RANGE.get(key, (5, 25))
        base  = random.uniform(lo, hi)
        val   = round(base * age_factor(p["date_of_birth"]), 1)
        val   = max(1.0, val)
        run("UPDATE Player SET market_value=%s WHERE player_id=%s", (val, p["player_id"]))
        gen_count += 1

    print(f"  Tahmine dayali deger atanan oyuncu: {gen_count}")

    # Dogrulama
    r = qone("""
        SELECT COUNT(*) AS toplam,
               COUNT(market_value) AS degeri_olan,
               ROUND(MIN(market_value),1) AS min_v,
               ROUND(MAX(market_value),1) AS max_v,
               ROUND(AVG(market_value),1) AS avg_v
        FROM Player
    """)
    print(f"\n  Toplam oyuncu       : {r['toplam']}")
    print(f"  Degeri olan         : {r['degeri_olan']}")
    print(f"  Min / Max / Ort (M€): {r['min_v']} / {r['max_v']} / {r['avg_v']}")

    # Top 10 en degerli
    top = qall("""
        SELECT CONCAT(p.first_name,' ',p.last_name) AS oyuncu,
               c.name AS kulup, p.position, p.market_value
        FROM Player p LEFT JOIN Club c ON p.club_id=c.club_id
        ORDER BY market_value DESC LIMIT 10
    """)
    print("\n  En Degerli 10 Oyuncu:")
    for i,r in enumerate(top,1):
        print(f"    {i:2}. {r['oyuncu']:<30} {r['kulup']:<25} €{r['market_value']}M")

if __name__ == "__main__":
    main()
