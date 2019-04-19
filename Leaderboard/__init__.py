import os
import psycopg2
import csh_ldap as ldap
from flask import Flask, render_template, request

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd() + "/Leaderboard/", "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd() + "/Leaderboard/", "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd() + "/Leaderboard/", "config.env.py"))

@app.route("/")
def order():
    return render_template("index.html", player=get_players())

@app.route('/foosballGame', methods=['POST'])
def foosballGamePost():
    instance = ldap.CSHLDAP(app.config["BIND_DN"], app.config["BIND_PW"])
    reqData = request.get_json()
    player1 = instance.get_member_ibutton(reqData["player1"]).cn
    player2 = instance.get_member_ibutton(reqData["player2"]).cn
    score1 = reqData["score1"]
    score2 = reqData["score2"]
    if player1 != player2 and player1 not None and player2 not None and (score1 == 10 or score2 == 10):
        conn = psycopg2.connect(host="https://postgres.csh.rit.edu/",database="Leaderboard",user=app.config["PSQL_USER"],password=app.config["PSQL_PW"])                
        c = conn.cursor()
        c.execute('SELECT * FROM games')
        lst = c.fetchall()

    
def get_elo_dictionary(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM games')
    lst = c.fetchall()
    d = {}
    for element in lst:
        if element[1] not in d:
            d[element[1]] = 2000
        if element[3] not in d:
            d[element[3]] = 2000
        winner = element[2] > element[4]
        elo1, elo2 = calculate_elo(d[element[1]], d[element[3]], winner)
        d[element[1]] = elo1
        d[element[3]] = elo2
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
    c.execute('SELECT * FROM games')
    lst = c.fetchall()
    points = {}
    games = {}
    ppg = {}
    for element in lst:
        if element[1] not in games:
            games[element[1]] = 1
        else:
            games[element[1]] += 1
        if element[3] not in games:
            games[element[3]] = 1
        else:
            games[element[3]] += 1
        if element[1] not in points:
            points[element[1]] = 0
        if element[3] not in points:
            points[element[3]] = 0
        points[element[1]] += element[2]
        points[element[3]] += element[4]
    for key in games:
        point = points[key]
        game_num = games[key]
        ppg[key] = round(point/game_num, 2)
    return ppg


def calculate_percent(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM games')
    lst = c.fetchall()
    total = {}
    games = {}
    win_perc = {}
    for element in lst:
        if element[1] not in total:
            total[element[1]] = 0
        if element[3] not in total:
            total[element[3]] = 0
        total[element[1]] += 1
        total[element[3]] += 1
        winner = element[2] > element[4]
        if winner:
            if element[1] not in games:
                games[element[1]] = 0
            games[element[1]] += 1
        else:
            if element[3] not in games:
                games[element[3]] = 0
            games[element[3]] += 1
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


def get_players():
    # start = time.time()
    instance = ldap.CSHLDAP(app.config["BIND_DN"], app.config["BIND_PW"])
    conn = psycopg2.connect(host="https://postgres.csh.rit.edu/",database="Leaderboard",user=app.config["DBUSER"],password=app.config["DBPASSWD"])
    elo = get_elo_dictionary(conn)
    ppg = calculate_ppg(conn)
    perc = calculate_percent(conn)
    player = compile_player(elo, ppg, perc)
    player_objects = []
    """
    test_object = {"uid": "sophia", "cn": "Sophia Lynch", "elo": 1999, "ppg": 9.0, "win_perc": 51.0}
    player_objects.append(test_object)
    """
    for key in player:
        member = instance.get_member(key, uid=True)
        player_object = {"uid": key, "cn": member.cn, "elo": player[key][0], "ppg": player[key][1], "win_perc": player[key][2]}
        player_objects.append(player_object)
    player_objects.sort(key=lambda item: item["ppg"], reverse=True)
    player_objects.sort(key=lambda item: item["win_perc"], reverse=True)
    player_objects.sort(key=lambda item: item["elo"], reverse=True)
    return player_objects
