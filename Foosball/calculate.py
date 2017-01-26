"""



"""


def calculate_elo(elo_1, elo_2, winner=(1, 2)):
    tran_rating1 = 10 ** (elo_1 / 400)
    tran_rating2 = 10 ** (elo_2 / 400)
    expected_score1 = tran_rating1 / (tran_rating1 + tran_rating2)
    expected_score2 = tran_rating2 / (tran_rating1 + tran_rating2)
    if winner == 1:
        score1 = 1
        score2 = 0
    elif winner == 2:
        score2 = 1
        score1 = 0
    elo_change_1 = elo_1 + (32 * (score1 - expected_score1))
    elo_change_2 = elo_2 + (32 * (score2 - expected_score2))
    return int(round(elo_change_1)), int(round(elo_change_2))


def calculate_ppg():
    pass


def calculate_percent():
    pass
