
# from csh_ldap import *
import RPi.GPIO as GPIO
import sqlite3 as s
from Leaderboard.calculate import *
import time


def play_game():
    score1 = 0
    score2 = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while score1 < 10 and score2 < 10:
        input1 = GPIO.input(4)
        input2 = GPIO.input(21)
        if input1 == False:
            score1 += 1
            time.sleep(0.2)
            while input1 == False:
                input1 = GPIO.input(4)
                time.sleep(0.2)
        if input2 == False:
            score2 += 1
            time.sleep(0.2)
            while input2 == False:
                input2 = GPIO.input(21)
                time.sleep(0.2)
    return score1, score2


def read_button():
    base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
    data = open(base_dir, "r")
    ibutton = data.read().strip()
    data.close()
    if ibutton != 'not found.\n':
        GPIO.output(14, False)
        time.sleep(1)
        return ibutton[3:] + "01"


def find_elo(tup, uid):
    for idx in range(len(tup)):
        if tup[idx] == uid:
            player_place = idx
            break
    if player_place == 0:
        elo_place = -2
    elif player_place == 1:
        elo_place = -1
    return tup[elo_place]


def delete(conn):
    prompt = str(input("Clear Table? (Y/N)"))
    if prompt == "Y":
        sql = "DELETE FROM games"
        conn.execute(sql)
        print("Deleting")
    elif prompt == "N":
        return False
    else:
        print("Invalid Command")
        return "Invalid"


def main():
    # instance = ldap.CSHLDAP("leaderboard", "reprimand5075$namely")

    conn = s.connect('../database.db')
    c = conn.cursor()

    """
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(7, GPIO.IN)
    """

    while True:
        # ibutton1 = read_button()
        # ibutton2 = read_button()
        # member1 = instance.get_member_ibutton(ibutton1)
        # member2 = instance.get_member_ibutton(ibutton2)
        member1 = str(input("Member 1: "))
        member2 = str(input("Member 2: "))
        if member1 is not None and member2 is not None:
            print("Game in progress")
            score1, score2 = play_game()
            UID1 = member1  # .uid
            UID2 = member2  # .uid
            '''
            c.execute('SELECT * FROM games WHERE player1 == "{}" or player2 == "{}"'.format(UID1, UID1))
            p1_lst = c.fetchall()
            c.execute('SELECT * FROM games WHERE player1 == "{}" or player2 == "{}"'.format(UID2, UID2))
            p2_lst = c.fetchall()
            if not p1_lst or not p2_lst:
                if not p1_lst:
                    elo_one = 2000
                if not p2_lst:
                    elo_two = 2000
            else:
                current_elo1 = find_elo(p1_lst[-1], UID1)
                current_elo2 = find_elo(p2_lst[-1], UID2)
                if score1 > score2:
                    winner = 1
                else:
                    winner = 2
                elo_one, elo_two = calculate_elo(current_elo1, current_elo2, winner)
            '''
            params = (UID1, score1, UID2,  score2)
            c.execute("INSERT INTO games VALUES (NULL, ?, ?, ?, ?)", params)
            c.execute("SELECT * FROM games")
            lst = c.fetchall()
            print(lst)
            delete(c)
            conn.commit()
        else:
            print("User not found")
    conn.close()
main()
