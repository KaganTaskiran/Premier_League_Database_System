"""
Club Deduplication Migration
premier_league_db - Merges duplicate club entries
"""

import mysql.connector

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "123456",
    "database": "premier_league_db",
    "charset":  "utf8mb4",
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

# (duplicate_id, canonical_id, new_canonical_name)
# Duplicates to merge INTO canonical
MERGES = [
    # Arsenal
    (35, 1, "Arsenal"),
    # Aston Villa
    (53, 8, "Aston Villa"),
    # Brentford
    (55, 19, "Brentford"),
    # Brighton
    (51, 10, "Brighton & Hove Albion"),
    (64, 10, "Brighton & Hove Albion"),  # "Brighton Hove" from football-data.org
    # Burnley
    (37, 16, "Burnley"),
    # Chelsea
    (31, 2, "Chelsea"),
    # Crystal Palace
    (42, 14, "Crystal Palace"),
    # Everton
    (27, 12, "Everton"),
    # Fulham
    (41, 21, "Fulham"),
    # Leeds United
    (43, 17, "Leeds United"),
    # Leicester City
    (47, 11, "Leicester City"),
    # Liverpool
    (34, 3, "Liverpool"),
    # Manchester City (merge Man City AND Manchester City FC)
    (25, 4, "Manchester City"),
    (54, 4, "Manchester City"),
    # Manchester United
    (52, 5, "Manchester United"),
    # Newcastle United
    (45, 7, "Newcastle United"),
    # Norwich City
    (56, 30, "Norwich City"),
    # Nottingham Forest
    (57, 20, "Nottingham Forest"),
    (63, 20, "Nottingham Forest"),  # "Nottingham" shortname
    # Sheffield United
    (49, 18, "Sheffield United"),
    # Southampton
    (33, 15, "Southampton"),
    # Sunderland: keep AFC Bournemouth-style "Sunderland AFC"(29) but rename to Sunderland
    # merge football-data shortname "Sunderland"(60) into AFC version (29)
    (60, 29, "Sunderland"),
    # AFC Bournemouth(26): rename to Bournemouth; merge Bournemouth(65) into it
    (65, 26, "Bournemouth"),
    # Tottenham
    (48, 6, "Tottenham Hotspur"),
    (61, 6, "Tottenham Hotspur"),  # "Tottenham" shortname
    # Watford
    (28, 23, "Watford"),
    # West Brom
    (46, 22, "West Bromwich Albion"),
    # West Ham
    (44, 9, "West Ham United"),
    # Wolverhampton
    (50, 13, "Wolverhampton Wanderers"),
    (62, 13, "Wolverhampton Wanderers"),  # "Wolverhampton" shortname
]

# Some canonical clubs need renaming too
RENAME_CANONICAL = {
    29: "Sunderland",
    26: "Bournemouth",
}

def merge_club(conn, dup_id, can_id):
    cur = conn.cursor()

    # 1. Match: home
    cur.execute("UPDATE `Match` SET home_club_id=%s WHERE home_club_id=%s", (can_id, dup_id))
    # 2. Match: away
    cur.execute("UPDATE `Match` SET away_club_id=%s WHERE away_club_id=%s", (can_id, dup_id))
    # 3. Player
    cur.execute("UPDATE Player SET club_id=%s WHERE club_id=%s", (can_id, dup_id))
    # 4. Coach
    cur.execute("UPDATE Coach SET club_id=%s WHERE club_id=%s", (can_id, dup_id))
    # 5. Transfer from
    cur.execute("UPDATE Transfer SET from_club_id=%s WHERE from_club_id=%s", (can_id, dup_id))
    # 6. Transfer to
    cur.execute("UPDATE Transfer SET to_club_id=%s WHERE to_club_id=%s", (can_id, dup_id))

    # 7. LeagueStandings - need to merge season by season
    cur.execute("SELECT * FROM LeagueStandings WHERE club_id=%s", (dup_id,))
    dup_standings = cur.fetchall()

    for row in dup_standings:
        # Check if canonical already has this season
        season = row[2]  # season column index
        cur.execute("SELECT * FROM LeagueStandings WHERE club_id=%s AND season=%s", (can_id, season))
        existing = cur.fetchone()
        if existing:
            # Merge: add stats together
            cur.execute("""
                UPDATE LeagueStandings SET
                    played        = played        + %s,
                    won           = won           + %s,
                    drawn         = drawn         + %s,
                    lost          = lost          + %s,
                    goals_for     = goals_for     + %s,
                    goals_against = goals_against + %s
                WHERE club_id=%s AND season=%s
            """, (row[3], row[4], row[5], row[6], row[7], row[8], can_id, season))
            cur.execute("DELETE FROM LeagueStandings WHERE club_id=%s AND season=%s", (dup_id, season))
        else:
            # Just re-assign
            cur.execute("UPDATE LeagueStandings SET club_id=%s WHERE club_id=%s AND season=%s",
                        (can_id, dup_id, season))

    # 8. Delete remaining standings for dup (shouldn't be any left)
    cur.execute("DELETE FROM LeagueStandings WHERE club_id=%s", (dup_id,))

    # 9. Delete the duplicate club
    cur.execute("DELETE FROM Club WHERE club_id=%s", (dup_id,))

    conn.commit()
    cur.close()

def main():
    conn = get_conn()
    print("=== Club Deduplication Migration ===\n")

    done = set()
    for dup_id, can_id, can_name in MERGES:
        if dup_id not in done:
            print(f"  Merging club_id={dup_id} into club_id={can_id} ({can_name})")
            try:
                merge_club(conn, dup_id, can_id)
                done.add(dup_id)
            except Exception as e:
                print(f"    ERROR: {e}")
                conn.rollback()

    # Rename canonical clubs where needed
    cur = conn.cursor()
    for cid, new_name in RENAME_CANONICAL.items():
        try:
            cur.execute("UPDATE Club SET name=%s WHERE club_id=%s", (new_name, cid))
            print(f"  Renamed club_id={cid} to '{new_name}'")
        except Exception as e:
            print(f"  Could not rename {cid}: {e}")
    conn.commit()
    cur.close()

    # Summary
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Club")
    clubs = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM `Match`")
    matches = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM LeagueStandings")
    standings = cur.fetchone()[0]
    cur.close()
    conn.close()

    print(f"\nMigration tamamlandi!")
    print(f"  Kulup: {clubs}")
    print(f"  Mac:   {matches}")
    print(f"  Puan Durumu: {standings}")

if __name__ == "__main__":
    main()
