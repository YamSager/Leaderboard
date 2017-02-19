from flask import Flask
from Leaderboard.calculate import main

app = Flask(__name__)


@app.route("/")
def order():
    player = main()
    return player
