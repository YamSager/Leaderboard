import psycopg2
import csh_ldap as ldap

def get_elo_dictionary(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM "foosballGame"')
    lst = c.fetchall()
    d = {}
    for element in lst:
        if element[1] not in d:
            d[element[1]] = 2000
        if element[2] not in d:
            d[element[2]] = 2000
        winner = element[3] > element[4]
        elo1, elo2 = calculate_elo(d[element[1]], d[element[2]], winner)
        d[element[1]] = elo1
        d[element[2]] = elo2
    return d


def calculate_elo(elo_1, elo_2, winner):
    tran_rating1 = 10 ** (elo_1 / 400)
    tran_rating2 = 10 ** (elo_2 / 400)
    expected_score1 = tran_rating1 / (tran_rating1 + tran_rating2)
    expected_score2 = tran_rating2 / (tran_rating1 + tran_rating2)
    if winner:
        score1 = 1
        score2 = 0
    else:
        score2 = 1
        score1 = 0
    elo_change_1 = elo_1 + (32 * (score1 - expected_score1))
    elo_change_2 = elo_2 + (32 * (score2 - expected_score2))
    return int(round(elo_change_1)), int(round(elo_change_2))


def calculate_ppg(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM "foosballGame"')
    lst = c.fetchall()
    points = {}
    games = {}
    ppg = {}
    for element in lst:
        if element[1] not in games:
            games[element[1]] = 1
        else:
            games[element[1]] += 1
        if element[2] not in games:
            games[element[2]] = 1
        else:
            games[element[2]] += 1
        if element[1] not in points:
            points[element[1]] = 0
        if element[2] not in points:
            points[element[2]] = 0
        points[element[1]] += element[3]
        points[element[2]] += element[4]
    for key in games:
        point = points[key]
        game_num = games[key]
        ppg[key] = round(point/game_num, 2)
    return ppg


def calculate_percent(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM "foosballGame"')
    lst = c.fetchall()
    total = {}
    games = {}
    win_perc = {}
    for element in lst:
        if element[1] not in total:
            total[element[1]] = 0
        if element[2] not in total:
            total[element[2]] = 0
        total[element[1]] += 1
        total[element[2]] += 1
        winner = element[3] > element[4]
        if winner:
            if element[1] not in games:
                games[element[1]] = 0
            games[element[1]] += 1
        else:
            if element[2] not in games:
                games[element[2]] = 0
            games[element[2]] += 1
    for key in total:
        if key not in games:
            wins = 0
        else:
            wins = games[key]
        total_games = total[key]
        win_perc[key] = round(wins/total_games*100, 2)
    return win_perc


def compile_player(elo, ppg, perc):
    player = {}
    for key in elo:
        player_elo = elo[key]
        player_points = ppg[key]
        player_wins = perc[key]
        player_tup = (player_elo, player_points, player_wins)
        player[key] = player_tup
    return player


def get_players(app):
    # start = time.time()
    instance = ldap.CSHLDAP(app.config["BIND_DN"], app.config["BIND_PW"])
    conn = psycopg2.connect(host="postgres.csh.rit.edu",database="leaderboard",user=app.config["PSQL_USER"],password=app.config["PSQL_PW"], options="-c search_path=public")
    elo = get_elo_dictionary(conn)
    ppg = calculate_ppg(conn)
    perc = calculate_percent(conn)
    player = compile_player(elo, ppg, perc)
    player_objects = []
    for key in player:
        member = instance.get_member_ibutton(key)
        player_object = {"uid": member.uid, "cn": member.cn, "elo": player[key][0], "ppg": player[key][1], "win_perc": player[key][2]}
        player_objects.append(player_object)
    player_objects.sort(key=lambda item: item["ppg"], reverse=True)
    player_objects.sort(key=lambda item: item["win_perc"], reverse=True)
    player_objects.sort(key=lambda item: item["elo"], reverse=True)
    print(player_objects)
    return player_objects
