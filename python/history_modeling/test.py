import pandas as pd


def get_match_info(row):
    # add adversary age & hand ?
    surface = row["tournament_surface"]
    result = row["Winner"]
    score = row["score"]
    num_played_minutes = row["minutes"]
    date = row["tourney_date"]

    adv_ranking = row["Ranking_2"]
    adv_ranking_points = row["Ranking_points_2"]

    num_won_sets = 0
    num_lost_sets = 0
    num_won_games = 0
    num_lost_games = 0
    num_tie_break_wons = 0
    num_tie_break_lost = 0

    for set in row["score"].split(" "):
        games_0 = set.split("-")[0]
        games_1 = set.split("-")[1]

        if "(" in games_0:
            tie_break_0 = games_0.split("(")[1].split(")")[0]
            games_0 = games_0.split("(")[0]

            tie_break_0 = int(tie_break_0)
            tie_break_1 = 7 if tie_break_0 <= 0 else tie_break_0 + 2
        elif "(" in games_1:
            tie_break_1 = games_1.split("(")[1].split(")")[0]
            games_1 = games_1.split("(")[0]

            tie_break_1 = int(tie_break_1)
            tie_break_0 = 7 if tie_break_1 <= 0 else tie_break_1 + 2

        else:
            tie_break_0 = 0
            tie_break_1 = 0

        games_0 = int(games_0)
        games_1 = int(games_1)

        if games_0 < games_1:
            num_won_sets += 1
        elif games_0 > games_1:
            num_lost_sets += 1
        elif tie_break_0 > tie_break_1:
            num_won_sets += 1
        else:
            num_lost_sets += 1

        num_won_games += games_0
        num_lost_games += games_1
        num_tie_break_wons += tie_break_0
        num_tie_break_lost += tie_break_1

    match_df = pd.DataFrame({
        "surface": [surface],
        "result": [result],
        "num_played_minutes": [num_played_minutes],
        "date": [date],
        "adv_ranking": [adv_ranking],
        "adv_ranking_points": [adv_ranking_points],
        "num_won_sets": [num_won_sets],
        "num_lost_sets": [num_lost_sets],
        "num_won_games": [num_won_games],
        "num_lost_games": [num_lost_games],
        "num_tie_break_wons": [num_tie_break_wons],
        "num_tie_break_lost": [num_tie_break_lost]
    })
    return match_df


def matches_info_norm(matches_info, current_date=""):

    tournament_surface = {"Clay": 0., "Carpet": 1/3, "Hard": 2/3, "Grass": 1.0}

    matches_info = matches_info.copy()
    matches_info["surface"] = matches_info["surface"].apply(lambda val: tournament_surface[val])
    matches_info["num_won_sets"] = matches_info["num_won_sets"].apply(lambda val: val / 3)
    matches_info["num_lost_sets"] = matches_info["num_lost_sets"].apply(lambda val: val / 3)

    matches_info["date"] = matches_info["date"].apply(lambda val: val / 3)
    matches_info["num_played_minutes"] = matches_info["num_played_minutes"].apply(lambda val: val / 3)

    matches_info["adv_ranking"] = matches_info["adv_ranking"].apply(lambda val: val / 3)
    matches_info["adv_ranking_points"] = matches_info["adv_ranking_points"].apply(lambda val: val / 3)

    matches_info["num_won_games"] = matches_info["num_won_games"].apply(lambda val: val / 3)
    matches_info["num_lost_games"] = matches_info["num_lost_games"].apply(lambda val: val / 3)
    matches_info["num_tie_break_wons"] = matches_info["num_tie_break_wons"].apply(lambda val: val / 3)
    matches_info["num_tie_break_lost"] = matches_info["num_tie_break_lost"].apply(lambda val: val / 3)

    return matches_info

