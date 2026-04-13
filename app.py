from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ---------------------------------------------------------------------------
# DB helper
# ---------------------------------------------------------------------------

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def query(sql, params=None, fetchone=False):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    result = cur.fetchone() if fetchone else cur.fetchall()
    cur.close()
    conn.close()
    return result


def execute(sql, params=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    last_id = cur.lastrowid
    cur.close()
    conn.close()
    return last_id


# ---------------------------------------------------------------------------
# DASHBOARD / INDEX
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    season = request.args.get('season', '2024/25')
    all_seasons = query("SELECT DISTINCT season FROM LeagueStandings ORDER BY season DESC")

    standings = query("""
        SELECT
            RANK() OVER (ORDER BY (ls.won*3+ls.drawn) DESC,
                         (ls.goals_for-ls.goals_against) DESC, ls.goals_for DESC) AS pos,
            c.name AS club, c.club_id,
            ls.played, ls.won, ls.drawn, ls.lost,
            ls.goals_for AS gf, ls.goals_against AS ga,
            (ls.goals_for-ls.goals_against) AS gd,
            (ls.won*3+ls.drawn) AS pts
        FROM LeagueStandings ls
        JOIN Club c ON ls.club_id = c.club_id
        WHERE ls.season = %s
        ORDER BY pts DESC, gd DESC, gf DESC
    """, (season,))

    top_scorers = query("""
        SELECT
            CONCAT(p.first_name,' ',p.last_name) AS player,
            p.player_id,
            COALESCE(c.name, 'N/A') AS club,
            SUM(ps.goals) AS goals,
            SUM(ps.assists) AS assists,
            COUNT(ps.match_id) AS matches
        FROM PlayerStatistics ps
        JOIN Player  p ON ps.player_id = p.player_id
        JOIN `Match` m ON ps.match_id  = m.match_id
        LEFT JOIN Club c ON p.club_id  = c.club_id
        WHERE m.season = %s
        GROUP BY p.player_id
        ORDER BY goals DESC, assists DESC
        LIMIT 5
    """, (season,))

    recent_matches = query("""
        SELECT
            m.match_id, m.match_date, m.gameweek, m.season,
            hc.name AS home_club, m.home_score,
            m.away_score, ac.name AS away_club
        FROM `Match` m
        JOIN Club hc ON m.home_club_id = hc.club_id
        JOIN Club ac ON m.away_club_id = ac.club_id
        WHERE m.season = %s
        ORDER BY m.match_date DESC
        LIMIT 5
    """, (season,))

    champions = query("""
        SELECT c.name AS club, COUNT(*) AS titles,
               GROUP_CONCAT(ls.season ORDER BY ls.season SEPARATOR ', ') AS seasons
        FROM LeagueStandings ls
        JOIN Club c ON ls.club_id = c.club_id
        WHERE (ls.won*3+ls.drawn) = (
            SELECT MAX(won*3+drawn) FROM LeagueStandings ls2 WHERE ls2.season=ls.season
        )
        GROUP BY c.club_id
        ORDER BY titles DESC
    """)

    active_injuries = query("""
        SELECT player_name, club, injury_type, days_injured
        FROM v_active_injuries
        ORDER BY days_injured DESC
        LIMIT 5
    """)

    return render_template('index.html',
                           standings=standings,
                           top_scorers=top_scorers,
                           season=season,
                           all_seasons=all_seasons,
                           champions=champions,
                           recent_matches=recent_matches,
                           active_injuries=active_injuries)


# ---------------------------------------------------------------------------
# CLUBS
# ---------------------------------------------------------------------------

@app.route('/clubs')
def clubs():
    season = request.args.get('season', '2024/25')
    all_seasons = query("SELECT DISTINCT season FROM `Match` ORDER BY season DESC")

    rows = query("""
        SELECT c.*,
               MAX(co.first_name) AS first_name,
               MAX(co.last_name)  AS last_name,
               COUNT(DISTINCT ps.player_id) AS squad_size
        FROM Club c
        LEFT JOIN Coach co ON co.club_id = c.club_id
        LEFT JOIN `Match` m ON (m.home_club_id = c.club_id OR m.away_club_id = c.club_id)
                             AND m.season = %s
        LEFT JOIN PlayerStatistics ps ON ps.match_id = m.match_id
        WHERE c.club_id IN (
            SELECT DISTINCT home_club_id FROM `Match` WHERE season = %s
            UNION
            SELECT DISTINCT away_club_id FROM `Match` WHERE season = %s
        )
        GROUP BY c.club_id, c.name, c.city, c.stadium, c.capacity, c.founded
        ORDER BY c.name
    """, (season, season, season))
    return render_template('clubs.html', clubs=rows, season=season, all_seasons=all_seasons)


@app.route('/clubs/<int:club_id>')
def club_detail(club_id):
    club = query("SELECT * FROM Club WHERE club_id = %s", (club_id,), fetchone=True)
    if not club:
        flash('Club not found.', 'danger')
        return redirect(url_for('clubs'))

    all_seasons = query("""
        SELECT DISTINCT m.season FROM `Match` m
        WHERE m.home_club_id = %s OR m.away_club_id = %s
        ORDER BY m.season DESC
    """, (club_id, club_id))

    season = request.args.get('season', '2024/25')
    available = [r['season'] for r in all_seasons]
    if season not in available and available:
        season = available[0]

    coach = query("SELECT * FROM Coach WHERE club_id = %s", (club_id,), fetchone=True)

    players = query("""
        SELECT p.player_id, p.first_name, p.last_name, p.nationality,
               p.position, p.jersey_number, p.market_value,
               TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()) AS age,
               SUM(ps.goals)          AS season_goals,
               SUM(ps.assists)        AS season_assists,
               COUNT(ps.match_id)     AS season_matches,
               SUM(ps.minutes_played) AS season_minutes
        FROM PlayerStatistics ps
        JOIN Player  p  ON ps.player_id = p.player_id
        JOIN `Match` m  ON ps.match_id  = m.match_id
        WHERE m.season = %s
          AND (m.home_club_id = %s OR m.away_club_id = %s)
        GROUP BY p.player_id
        ORDER BY FIELD(p.position,'Goalkeeper','Defender','Midfielder','Forward'),
                 season_goals DESC
    """, (season, club_id, club_id))

    matches = query("""
        SELECT m.match_id, m.match_date, m.gameweek, m.season,
               hc.name AS home_club, m.home_score,
               m.away_score, ac.name AS away_club
        FROM `Match` m
        JOIN Club hc ON m.home_club_id = hc.club_id
        JOIN Club ac ON m.away_club_id = ac.club_id
        WHERE (m.home_club_id = %s OR m.away_club_id = %s)
          AND m.season = %s
        ORDER BY m.match_date DESC
    """, (club_id, club_id, season))

    standings = query("""
        SELECT played, won, drawn, lost, goals_for, goals_against,
               (goals_for - goals_against) AS gd,
               (won*3+drawn) AS pts
        FROM LeagueStandings WHERE club_id = %s AND season = %s
    """, (club_id, season), fetchone=True)

    return render_template('club_detail.html',
                           club=club, coach=coach,
                           players=players, matches=matches,
                           standings=standings,
                           season=season,
                           all_seasons=all_seasons)


# ---------------------------------------------------------------------------
# PLAYERS
# ---------------------------------------------------------------------------

@app.route('/players')
def players():
    pos_filter  = request.args.get('position', '')
    club_filter = request.args.get('club_id', '')
    search      = request.args.get('search', '')

    sql = """
        SELECT p.player_id, CONCAT(p.first_name,' ',p.last_name) AS full_name,
               p.nationality, p.position, p.jersey_number,
               TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()) AS age,
               c.name AS club, p.market_value
        FROM Player p
        LEFT JOIN Club c ON p.club_id = c.club_id
        WHERE 1=1
    """
    params = []
    if pos_filter:
        sql += " AND p.position = %s"
        params.append(pos_filter)
    if club_filter:
        sql += " AND p.club_id = %s"
        params.append(club_filter)
    if search:
        sql += " AND (p.first_name LIKE %s OR p.last_name LIKE %s)"
        params += [f'%{search}%', f'%{search}%']
    sql += " ORDER BY c.name, p.position, p.last_name"

    player_list = query(sql, params)
    all_clubs   = query("SELECT club_id, name FROM Club ORDER BY name")
    return render_template('players.html',
                           players=player_list,
                           all_clubs=all_clubs,
                           pos_filter=pos_filter,
                           club_filter=club_filter,
                           search=search)


@app.route('/players/<int:player_id>')
def player_detail(player_id):
    player = query("""
        SELECT p.*,
               TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()) AS age,
               c.name AS club_name
        FROM Player p
        LEFT JOIN Club c ON p.club_id = c.club_id
        WHERE p.player_id = %s
    """, (player_id,), fetchone=True)
    if not player:
        flash('Player not found.', 'danger')
        return redirect(url_for('players'))

    stats = query("""
        SELECT m.match_date, m.season, m.gameweek,
               hc.name AS home_club, m.home_score,
               m.away_score, ac.name AS away_club,
               ps.goals, ps.assists, ps.yellow_cards,
               ps.red_cards, ps.minutes_played, ps.shots_on_target
        FROM PlayerStatistics ps
        JOIN `Match` m  ON ps.match_id  = m.match_id
        JOIN Club   hc  ON m.home_club_id = hc.club_id
        JOIN Club   ac  ON m.away_club_id = ac.club_id
        WHERE ps.player_id = %s
        ORDER BY m.match_date DESC
    """, (player_id,))

    season_totals = query("""
        SELECT m.season,
               COUNT(ps.match_id)     AS matches,
               SUM(ps.goals)          AS goals,
               SUM(ps.assists)        AS assists,
               SUM(ps.yellow_cards)   AS yellows,
               SUM(ps.red_cards)      AS reds,
               SUM(ps.minutes_played) AS minutes
        FROM PlayerStatistics ps
        JOIN `Match` m ON ps.match_id = m.match_id
        WHERE ps.player_id = %s
        GROUP BY m.season ORDER BY m.season DESC
    """, (player_id,))

    transfers = query("""
        SELECT t.transfer_date, t.season, t.transfer_fee,
               COALESCE(fc.name,'Free Agent') AS from_club,
               tc.name AS to_club
        FROM Transfer t
        LEFT JOIN Club fc ON t.from_club_id = fc.club_id
        JOIN Club tc ON t.to_club_id = tc.club_id
        WHERE t.player_id = %s ORDER BY t.transfer_date DESC
    """, (player_id,))

    injuries = query("""
        SELECT injury_type, start_date, end_date, matches_missed
        FROM Injury WHERE player_id = %s ORDER BY start_date DESC
    """, (player_id,))

    return render_template('player_detail.html',
                           player=player, stats=stats,
                           season_totals=season_totals,
                           transfers=transfers, injuries=injuries)


@app.route('/players/add', methods=['GET', 'POST'])
def add_player():
    all_clubs = query("SELECT club_id, name FROM Club ORDER BY name")
    if request.method == 'POST':
        try:
            execute("""
                INSERT INTO Player
                    (first_name, last_name, nationality, date_of_birth,
                     position, jersey_number, club_id, market_value, contract_end)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                request.form['first_name'],
                request.form['last_name'],
                request.form.get('nationality'),
                request.form.get('date_of_birth') or None,
                request.form['position'],
                request.form.get('jersey_number') or None,
                request.form.get('club_id') or None,
                request.form.get('market_value') or None,
                request.form.get('contract_end') or None,
            ))
            flash('Player added successfully!', 'success')
            return redirect(url_for('players'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('add_player.html', all_clubs=all_clubs)


# ---------------------------------------------------------------------------
# MATCHES
# ---------------------------------------------------------------------------

@app.route('/matches')
def matches():
    season = request.args.get('season', '2024/25')
    rows = query("""
        SELECT m.match_id, m.match_date, m.gameweek, m.season,
               hc.name AS home_club, hc.club_id AS home_id,
               m.home_score, m.away_score,
               ac.name AS away_club, ac.club_id AS away_id
        FROM `Match` m
        JOIN Club hc ON m.home_club_id = hc.club_id
        JOIN Club ac ON m.away_club_id = ac.club_id
        WHERE m.season = %s
        ORDER BY COALESCE(m.gameweek, 99), m.match_date
    """, (season,))

    seasons = query("SELECT DISTINCT season FROM `Match` ORDER BY season DESC")
    return render_template('matches.html', matches=rows,
                           season=season, seasons=seasons)


@app.route('/matches/add', methods=['GET', 'POST'])
def add_match():
    all_clubs = query("SELECT club_id, name FROM Club ORDER BY name")
    if request.method == 'POST':
        try:
            mid = execute("""
                INSERT INTO `Match`
                    (home_club_id, away_club_id, match_date, home_score, away_score, season, gameweek)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                request.form['home_club_id'],
                request.form['away_club_id'],
                request.form['match_date'],
                request.form.get('home_score', 0),
                request.form.get('away_score', 0),
                request.form['season'],
                request.form.get('gameweek') or None,
            ))
            conn = get_db()
            cur = conn.cursor()
            cur.callproc('sp_update_standings', (mid,))
            conn.commit()
            cur.close()
            conn.close()
            flash('Match added and standings updated!', 'success')
            return redirect(url_for('matches'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('add_match.html', all_clubs=all_clubs)


# ---------------------------------------------------------------------------
# MATCH DETAIL
# ---------------------------------------------------------------------------

@app.route('/matches/<int:match_id>')
def match_detail(match_id):
    match = query("""
        SELECT m.*, hc.name AS home_club, hc.club_id AS home_club_id,
               ac.name AS away_club, ac.club_id AS away_club_id
        FROM `Match` m
        JOIN Club hc ON m.home_club_id = hc.club_id
        JOIN Club ac ON m.away_club_id = ac.club_id
        WHERE m.match_id = %s
    """, (match_id,), fetchone=True)
    if not match:
        flash('Maç bulunamadı.', 'danger')
        return redirect(url_for('matches'))

    events = query("""
        SELECT ge.*, CONCAT(p.first_name,' ',p.last_name) AS player_name
        FROM GameEvent ge
        LEFT JOIN Player p ON ge.player_id = p.player_id
        WHERE ge.match_id = %s ORDER BY ge.minute
    """, (match_id,))

    home_events = [e for e in events if e['club_id'] == match['home_club_id']]
    away_events = [e for e in events if e['club_id'] == match['away_club_id']]

    lineup = query("""
        SELECT * FROM GameLineup WHERE match_id = %s ORDER BY type, number
    """, (match_id,))

    home_lineup = [l for l in lineup if l['club_id'] == match['home_club_id']]
    away_lineup = [l for l in lineup if l['club_id'] == match['away_club_id']]

    player_stats = query("""
        SELECT ps.*, CONCAT(p.first_name,' ',p.last_name) AS player_name,
               c.name AS club
        FROM PlayerStatistics ps
        JOIN Player p ON ps.player_id = p.player_id
        LEFT JOIN Club c ON p.club_id = c.club_id
        WHERE ps.match_id = %s
    """, (match_id,))

    return render_template('match_detail.html',
        match=match,
        home_events=home_events, away_events=away_events,
        home_lineup=home_lineup, away_lineup=away_lineup,
        player_stats=player_stats)


# ---------------------------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------------------------

@app.route('/statistics')
def statistics():
    season = request.args.get('season', '2024/25')

    top_scorers = query("""
        SELECT
            CONCAT(p.first_name,' ',p.last_name) AS player,
            p.player_id, p.nationality, p.position,
            c.name AS club,
            SUM(ps.goals)          AS goals,
            SUM(ps.assists)        AS assists,
            COUNT(ps.match_id)     AS matches,
            SUM(ps.minutes_played) AS minutes
        FROM PlayerStatistics ps
        JOIN Player  p ON ps.player_id = p.player_id
        JOIN `Match` m ON ps.match_id  = m.match_id
        JOIN Club    c ON p.club_id    = c.club_id
        WHERE m.season = %s
        GROUP BY p.player_id
        ORDER BY goals DESC, assists DESC
    """, (season,))

    top_assisters = query("""
        SELECT
            CONCAT(p.first_name,' ',p.last_name) AS player,
            p.player_id, c.name AS club,
            SUM(ps.assists) AS assists,
            SUM(ps.goals)   AS goals
        FROM PlayerStatistics ps
        JOIN Player  p ON ps.player_id = p.player_id
        JOIN `Match` m ON ps.match_id  = m.match_id
        JOIN Club    c ON p.club_id    = c.club_id
        WHERE m.season = %s
        GROUP BY p.player_id
        ORDER BY assists DESC, goals DESC
        LIMIT 10
    """, (season,))

    club_stats = query("""
        SELECT
            c.name AS club,
            SUM(ps.goals)   AS total_goals,
            SUM(ps.assists) AS total_assists,
            COUNT(DISTINCT ps.match_id) AS match_appearances,
            ROUND(SUM(ps.goals)/COUNT(DISTINCT ps.match_id),2) AS goals_per_match
        FROM PlayerStatistics ps
        JOIN Player  p ON ps.player_id = p.player_id
        JOIN `Match` m ON ps.match_id  = m.match_id
        JOIN Club    c ON p.club_id    = c.club_id
        WHERE m.season = %s
        GROUP BY c.club_id
        ORDER BY total_goals DESC
    """, (season,))

    seasons = query("SELECT DISTINCT season FROM `Match` ORDER BY season DESC")
    return render_template('statistics.html',
                           top_scorers=top_scorers,
                           top_assisters=top_assisters,
                           club_stats=club_stats,
                           season=season, seasons=seasons)


# ---------------------------------------------------------------------------
# TRANSFERS
# ---------------------------------------------------------------------------

@app.route('/transfers')
def transfers():
    rows = query("""
        SELECT t.transfer_id, t.transfer_date, t.season,
               CONCAT(p.first_name,' ',p.last_name) AS player,
               p.player_id, p.position, p.nationality,
               COALESCE(fc.name,'Free Agent') AS from_club,
               tc.name AS to_club,
               t.transfer_fee
        FROM Transfer t
        JOIN Player   p  ON t.player_id    = p.player_id
        LEFT JOIN Club fc ON t.from_club_id = fc.club_id
        JOIN Club     tc ON t.to_club_id   = tc.club_id
        ORDER BY t.transfer_date DESC
    """)
    all_clubs   = query("SELECT club_id, name FROM Club ORDER BY name")
    all_players = query("SELECT player_id, first_name, last_name FROM Player ORDER BY last_name")
    return render_template('transfers.html', transfers=rows,
                           all_clubs=all_clubs, all_players=all_players)


@app.route('/transfers/add', methods=['POST'])
def add_transfer():
    try:
        execute("""
            INSERT INTO Transfer (player_id, from_club_id, to_club_id, transfer_date, transfer_fee, season)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            request.form['player_id'],
            request.form.get('from_club_id') or None,
            request.form['to_club_id'],
            request.form['transfer_date'],
            request.form.get('transfer_fee') or None,
            request.form.get('season') or None,
        ))
        flash('Transfer recorded successfully!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('transfers'))


# ---------------------------------------------------------------------------
# INJURIES
# ---------------------------------------------------------------------------

@app.route('/injuries')
def injuries():
    all_injuries = query("""
        SELECT i.injury_id,
               CONCAT(p.first_name,' ',p.last_name) AS player,
               p.player_id, p.position,
               c.name AS club, i.injury_type,
               i.start_date, i.end_date, i.matches_missed,
               DATEDIFF(CURDATE(), i.start_date) AS days_injured,
               CASE WHEN i.end_date IS NULL OR i.end_date >= CURDATE()
                    THEN 'Active' ELSE 'Recovered' END AS status
        FROM Injury i
        JOIN Player p ON i.player_id = p.player_id
        LEFT JOIN Club c ON p.club_id = c.club_id
        ORDER BY i.start_date DESC
    """)
    all_players = query("SELECT player_id, first_name, last_name FROM Player ORDER BY last_name")
    return render_template('injuries.html', injuries=all_injuries, all_players=all_players)


@app.route('/injuries/add', methods=['POST'])
def add_injury():
    try:
        execute("""
            INSERT INTO Injury (player_id, injury_type, start_date, end_date, matches_missed)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            request.form['player_id'],
            request.form['injury_type'],
            request.form['start_date'],
            request.form.get('end_date') or None,
            request.form.get('matches_missed') or 0,
        ))
        flash('Injury record added!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('injuries'))


# ---------------------------------------------------------------------------
# ANALYTICAL QUERIES PAGE
# ---------------------------------------------------------------------------

@app.route('/queries')
def analytical_queries():
    nationality = query("""
        SELECT p.nationality, COUNT(*) AS player_count
        FROM Player p GROUP BY p.nationality ORDER BY player_count DESC
    """)

    avg_value = query("""
        SELECT position,
               ROUND(AVG(market_value),2) AS avg_value,
               COUNT(*) AS count
        FROM Player WHERE market_value IS NOT NULL
        GROUP BY position ORDER BY avg_value DESC
    """)

    squad_value = query("""
        SELECT c.name AS club,
               COUNT(p.player_id) AS players,
               SUM(p.market_value) AS total_value
        FROM Player p JOIN Club c ON p.club_id = c.club_id
        WHERE p.market_value IS NOT NULL
        GROUP BY c.club_id ORDER BY total_value DESC
    """)

    contributions = query("""
        SELECT
            CONCAT(p.first_name,' ',p.last_name) AS player,
            c.name AS club,
            SUM(ps.goals) AS goals, SUM(ps.assists) AS assists,
            SUM(ps.goals)+SUM(ps.assists) AS contributions
        FROM PlayerStatistics ps
        JOIN Player  p ON ps.player_id = p.player_id
        JOIN `Match` m ON ps.match_id  = m.match_id
        JOIN Club    c ON p.club_id    = c.club_id
        WHERE m.season='2024/25'
        GROUP BY p.player_id
        ORDER BY contributions DESC LIMIT 10
    """)

    return render_template('queries.html',
                           nationality=nationality,
                           avg_value=avg_value,
                           squad_value=squad_value,
                           contributions=contributions)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
