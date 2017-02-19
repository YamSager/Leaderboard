"""



"""
import sqlite3 as s
from Leaderboard.ranking import *


def get_elo_dictionary():
    conn = s.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games')
    lst = c.fetchall()
    d = {}
    for element in lst:
        if element[1] not in d:
            d[element[1]] = 2000
        if element[3] not in d:
            d[element[3]] = 2000
        winner = element[2] > element[4]
        elo1, elo2 = calculate_elo(d[element[1]], d[element[3]], winner)
        d[element[1]] = elo1
        d[element[3]] = elo2
    return d


def calculate_elo(elo_1, elo_2, winner):
    tran_rating1 = 10 ** (elo_1 / 400)
    tran_rating2 = 10 ** (elo_2 / 400)
    expected_score1 = tran_rating1 / (tran_rating1 + tran_rating2)
    expected_score2 = tran_rating2 / (tran_rating1 + tran_rating2)
    if winner:
        score1 = 1
        score2 = 0
    else:
        score2 = 1
        score1 = 0
    elo_change_1 = elo_1 + (32 * (score1 - expected_score1))
    elo_change_2 = elo_2 + (32 * (score2 - expected_score2))
    return int(round(elo_change_1)), int(round(elo_change_2))


def calculate_ppg():
    conn = s.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games')
    lst = c.fetchall()
    points = {}
    games = {}
    ppg = {}
    for element in lst:
        if element[1] not in games:
            games[element[1]] = 1
        else:
            games[element[1]] += 1
        if element[3] not in games:
            games[element[3]] = 1
        else:
            games[element[3]] += 1
        if element[1] not in points:
            points[element[1]] = 0
        if element[3] not in points:
            points[element[3]] = 0
        points[element[1]] += element[2]
        points[element[3]] += element[4]
    for key in games:
        point = points[key]
        game_num = games[key]
        ppg[key] = point/game_num
    return ppg


def calculate_percent():
    conn = s.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games')
    lst = c.fetchall()
    total = {}
    games = {}
    win_perc = {}
    for element in lst:
        if element[1] not in total:
            total[element[1]] = 0
        if element[3] not in total:
            total[element[3]] = 0
        total[element[1]] += 1
        total[element[3]] += 1
        winner = element[2] > element[4]
        if winner:
            if element[1] not in games:
                games[element[1]] = 0
            games[element[1]] += 1
        else:
            if element[3] not in games:
                games[element[3]] = 0
            games[element[3]] += 1
    for key in total:
        if key not in games:
            wins = 0
        else:
            wins = games[key]
        total_games = total[key]
        win_perc[key] = wins/total_games*100
    return win_perc


def compile_player(elo, ppg, perc):
    player = {}
    for key in elo:
        player_elo = elo[key]
        player_points = ppg[key]
        player_wins = perc[key]
        player_tup = (player_elo, player_points, player_wins)
        player[key] = player_tup
    return player


def main():
    # start = time.time()
    elo = get_elo_dictionary()
    ppg = calculate_ppg()
    perc = calculate_percent()
    player = compile_player(elo, ppg, perc)
    player_list = []
    for key in player:
        player_object = (key, player[key][0], player[key][1], player[key][2])
        player_list.append(player_object)
    # print(player_list)
    sorted_player = merge_sort(player_list)
    '''
    end = time.time()
    i = 0
    for element in sorted_player:
        i += 1
        print(str(i) + ". " + str(element))
    print("That only took " + str(end - start) + " seconds")
    '''
    return sorted_player

if __name__ == "__main__":
    main()
