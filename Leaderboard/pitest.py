from csh_ldap import *
from Leaderboard.Pi_main import read_button

instance = CSHLDAP("leaderboard", "reprimand5075$namely")
ibutton1 = read_button()
print(instance.get_member_ibutton(ibutton1))
