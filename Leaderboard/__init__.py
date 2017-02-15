from flask import Flask
from calculate import *

app = Flask(__name__)


@app.route("/")
def order():
    player = main()
    return player
