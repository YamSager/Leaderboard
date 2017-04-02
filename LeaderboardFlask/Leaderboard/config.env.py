"""
import os

# Flask config
DEBUG=False
IP=os.environ.get('IP', '0.0.0.0')
PORT=os.environ.get('PORT', '8080')
SERVER_NAME = os.environ.get('LEADERBOARD_NAME', 'leaderboard.csh.rit.edu:443')

LDAP_BIND_DN=os.environ.get('BIND_DN', 'cn=leaderboard,ou=Apps,dc=csh,dc=rit,dc=edu')
LDAP_BIND_PW=os.environ.get('BIND_PW', '')
"""
