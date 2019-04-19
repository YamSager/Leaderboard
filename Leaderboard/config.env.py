import os

# Flask config
DEBUG=False
IP=os.environ.get('IP', '0.0.0.0')
PORT=os.environ.get('PORT', '8080')
SERVER_NAME = os.environ.get('LEADERBOARD_NAME', 'leaderboard.csh.rit.edu:443')

BIND_DN=os.environ["BIND_DN"]
BIND_PW=os.environ["BIND_PW"]

PSQL_USER=os.environ["PSQL_USER"]
PSQL_PW=os.environ["PSQL_PW"]
