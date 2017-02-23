from flask import Flask, render_template
from Leaderboard.calculate import get_players

app = Flask(__name__)


@app.route("/")
def order():
    player = get_players()
    return render_template("index.html", player=player, )
