"""
2024/25 sezonu için PlayerStatistics yeniden üretimi
- Sadece gerçekten aktif (doğum yılı >= 1985) ve anlamlı değeri (>= 1.5M€) olan oyuncular
- Realitiye yakın dağılım: golcüler öne çıkıyor
"""
import mysql.connector, random, sys, io
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB = {"host":"localhost","user":"root","password":"123456",
      "database":"premier_league_db","charset":"utf8mb4"}

def conn(): return mysql.connector.connect(**DB)
def qall(sql,p=()):
    c=conn();cur=c.cursor(dictionary=True);cur.execute(sql,p);r=cur.fetchall();cur.close();c.close();return r
def runmany(sql,data):
    c=conn();cur=c.cursor();cur.executemany(sql,data);c.commit();n=cur.rowcount;cur.close();c.close();return n

random.seed(2025)

# 2024/25 maçları
matches = qall("""
    SELECT match_id, home_club_id, away_club_id, home_score, away_score
    FROM `Match` WHERE season='2024/25' ORDER BY match_id
""")

# Aktif oyuncular — 2024/25 için gerçekçi filtre:
# market_value >= 3M (PL'de oynayan biri bu değerin altında olmaz)
all_players = qall("""
    SELECT player_id, club_id, position, market_value, date_of_birth
    FROM Player
    WHERE market_value >= 3.0
      AND position IS NOT NULL
      AND date_of_birth >= '1982-01-01'
""")

print(f"Aktif oyuncu havuzu: {len(all_players)}")

# Her oyuncu için ağırlık: piyasa değeri yüksek = daha anahtar oyuncu
club_pos = {}
player_weight = {}
for p in all_players:
    cid = p["club_id"]; pos = p["position"]
    mv  = float(p["market_value"] or 3.0)
    pid = p["player_id"]
    club_pos.setdefault(cid, {}).setdefault(pos, []).append(pid)
    # Ağırlık: golcüler için değer daha fazla önem taşıyor
    if pos == "Forward":
        player_weight[pid] = max(1, int(mv / 8))
    elif pos == "Midfielder":
        player_weight[pid] = max(1, int(mv / 12))
    else:
        player_weight[pid] = 1

# Sezon boyunca oyuncu başına maksimum gol takibi (gerçekçi sınır)
season_goals = {}  # pid -> toplam gol
MAX_SEASON_GOALS = {
    "Forward":    22,   # top golcü 20-25 arası
    "Midfielder": 12,
    "Defender":   5,
    "Goalkeeper": 1,
}

batch   = []
existing = set()

def weighted_choice(players):
    weights = [player_weight.get(p, 1) for p in players]
    return random.choices(players, weights=weights, k=1)[0]

for m in matches:
    mid = m["match_id"]
    for cid, goals in [(m["home_club_id"], m["home_score"]),
                       (m["away_club_id"],  m["away_score"])]:
        if cid not in club_pos: continue

        fwd  = club_pos[cid].get("Forward",    [])
        midp = club_pos[cid].get("Midfielder", [])
        dfd  = club_pos[cid].get("Defender",   [])
        gkp  = club_pos[cid].get("Goalkeeper", [])
        if not (fwd or midp): continue

        def pick(pool, n):
            uniq = list(set(pool))
            return random.sample(uniq, min(n, len(uniq)))

        squad = pick(gkp,1) + pick(dfd,4) + pick(midp,4) + pick(fwd,3)
        extras = [p for p in list(set(fwd+midp+dfd+gkp)) if p not in squad]
        squad += pick(extras, 3)
        squad = list(dict.fromkeys(squad))

        # Gol dağıtımı — ağırlıklı seçim + sezon limiti
        goal_pool = fwd * 3 + midp
        scorers = {}
        for _ in range(goals):
            if not goal_pool: break
            # Sezon limitine ulaşmış oyuncuları havuzdan çıkar
            eligible = [p for p in goal_pool
                        if season_goals.get(p, 0) < MAX_SEASON_GOALS.get(
                            next((pl["position"] for pl in all_players if pl["player_id"]==p), "Forward"),
                            10)]
            if not eligible: eligible = goal_pool  # sınır doluysa yine de devam
            s = weighted_choice(eligible)
            scorers[s] = scorers.get(s, 0) + 1
            season_goals[s] = season_goals.get(s, 0) + 1

        # Asist
        asst_pool = fwd + midp * 2 + dfd
        assisters = {}
        for _ in range(sum(scorers.values())):
            if asst_pool and random.random() < 0.72:
                a = weighted_choice(asst_pool)
                assisters[a] = assisters.get(a, 0) + 1

        yc = random.sample(squad, min(random.randint(0,2), len(squad)))
        rc = random.choice(squad) if random.random() < 0.04 else None

        for pid in squad:
            if (mid, pid) in existing: continue
            g   = scorers.get(pid, 0)
            a   = assisters.get(pid, 0)
            yc_ = 1 if pid in yc else 0
            rc_ = 1 if pid == rc else 0
            mins = 90 if pid in (gkp[:1] if gkp else []) else \
                   random.randint(65,90) if pid in squad[:11] else \
                   random.randint(15,45)
            sot = g + (random.randint(0,2) if pid in set(fwd+midp) else 0)
            batch.append((pid, mid, g, a, yc_, rc_, mins, sot))
            existing.add((mid, pid))

n = runmany("""
    INSERT IGNORE INTO PlayerStatistics
    (player_id,match_id,goals,assists,yellow_cards,red_cards,minutes_played,shots_on_target)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
""", batch)

print(f"Eklenen stat: {n}")

# Top 10 gol krali 2024/25
top = qall("""
    SELECT CONCAT(p.first_name,' ',p.last_name) AS oyuncu,
           c.name AS kulup, p.position, p.market_value,
           SUM(ps.goals) AS goller, SUM(ps.assists) AS asistler
    FROM PlayerStatistics ps
    JOIN Player p  ON ps.player_id = p.player_id
    JOIN `Match` m ON ps.match_id  = m.match_id
    LEFT JOIN Club c ON p.club_id  = c.club_id
    WHERE m.season = '2024/25'
    GROUP BY p.player_id
    ORDER BY goller DESC, asistler DESC
    LIMIT 10
""")

print("\n2024/25 Top 10 Gol Krali:")
for i,r in enumerate(top,1):
    print(f"  {i:2}. {r['oyuncu']:<30} {r['kulup']:<25} {r['goller']}G {r['asistler']}A  €{r['market_value']}M")

print("\nTamamlandi!")
