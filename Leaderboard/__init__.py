import uuid
import os
import psycopg2
import csh_ldap as ldap
from flask import Flask, render_template, request
from Leaderboard.foosball import get_players

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd() + "/Leaderboard/", "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd() + "/Leaderboard/", "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd() + "/Leaderboard/", "config.env.py"))

@app.route("/")
def order():
    return render_template("index.html", player=get_players(app))

@app.route('/foosballGame', methods=['POST'])
def foosballGamePost():
    #try:
        reqData = request.get_json()
        player1 = reqData["player1"]
        player2 = reqData["player2"]
        score1 = int(reqData["score1"])
        score2 = int(reqData["score2"])
        if player1 != player2 and player1 is not None and player2 is not None and (score1 == 10 or score2 == 10):
            conn = psycopg2.connect(host="postgres.csh.rit.edu",database="leaderboard",user=app.config["PSQL_USER"],password=app.config["PSQL_PW"],options="-c search_path=public")                
            c = conn.cursor()
            c.execute('SELECT count(*) FROM "foosballGame"')
            count = c.fetchone()
            count = int(count[0]) + 1
            c.execute("INSERT INTO 'foosballGame' (id, player1, player2, score1, score2) VALUES (" + str(count) + ", '" + player1 + "', '" + player2 + "', " + str(score1) + ", " + str(score2) + ")")
            conn.commit()
            return "200"
        else:
            return "400 - Invalid game"
   # except:
    #   return "400 - Invalid format"
