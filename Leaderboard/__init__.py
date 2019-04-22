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
    try:
        reqData = request.get_json()
        player1 = reqData["player1"]
        player2 = reqData["player2"]
        score1 = reqData["score1"]
        score2 = reqData["score2"]
        if player1 != player2 and player1 is not None and player2 is not None and (score1 == 10 or score2 == 10):
            conn = psycopg2.connect(host="postgres.csh.rit.edu",database="leaderboard",user=app.config["PSQL_USER"],password=app.config["PSQL_PW"],options="-c search_path=public")                
            c = conn.cursor()
            c.execute('INSERT INTO "foosballGame"("player1", "player2", "score1", "score2") VALUES ("' + player1 + '", "' + player2 + '", ' + str(score1) + ', ' + str(score2) + ')')
            return "200"
        else:
            return "400"
    except:
        return "400"
