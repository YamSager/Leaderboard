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
    return render_template("index.html", player=get_players())

@app.route('/foosballGame', methods=['POST'])
def foosballGamePost():
    instance = ldap.CSHLDAP(app.config["BIND_DN"], app.config["BIND_PW"])
    reqData = request.get_json()
    player1 = instance.get_member_ibutton(reqData["player1"]).cn
    player2 = instance.get_member_ibutton(reqData["player2"]).cn
    score1 = reqData["score1"]
    score2 = reqData["score2"]
    if player1 != player2 and player1 is not None and player2 is not None and (score1 == 10 or score2 == 10):
        conn = psycopg2.connect(host="postgres.csh.rit.edu",database="leaderboard",user=app.config["PSQL_USER"],password=app.config["PSQL_PW"],options="-c search_path=public")                
        c = conn.cursor()
        c.execute('SELECT * FROM games')
        lst = c.fetchall()
