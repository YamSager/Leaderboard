import os
from flask import Flask, render_template
from Leaderboard.calculate import get_players

app = Flask(__name__)

app.config.from_pyfile(os.path.join(os.getcwd(), "../../LeaderboardFlask/Leaderboard/config.py"))


@app.route("/")
def order():
    player = get_players()
    return render_template("index.html", player=player)