"""



"""

from sqlite3 import *
from HTML import *
from csh_ldap import *


def get_table():
    d = dict
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    a_list = cur.fetchall()
    for lst in a_list:
        d[str(lst[0])] = lst[4]
        d[str(lst[1])] = lst[5]
    return d


def quick_sort(lst):
    if not lst:
        return lst
    else:
        low, same, high = quick_split(lst[0], lst)
        return quick_sort(low) + same + quick_sort(high)


def quick_split(pivot, lst):
    low, same, high = [], [], []
    for element in lst:
        if element[1] < pivot[0]:
            low.append(element)
        elif element[1] > pivot[0]:
            high.append(element)
        else:
            same.append(element)
    return low, same, high


def make_table(dic):
    table = []
    for key, value in dic.items():
        instance = CSHLDAP("leaderboard", "reprimand5075$namely")
        player = instance.get_member_ibutton(key)
        lst = [player, value]
        table.append(lst)
    sorted_table = quick_sort(table)
    html_code = HTML.table(sorted_table, header_row=['Player', 'Elo'])
    return html_code
