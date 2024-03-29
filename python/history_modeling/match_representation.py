import numpy as np
import pandas as pd

from data.data_utils import get_days_difference


def get_match_info(row, verbose=0):
    # add adversary age & hand ?
    surface = row["tournament_surface"]
    result = row["Winner"]
    try:
        score = row["score"]
    except:
        print(row)
        print(row.index)
        print(row.values)
    num_played_minutes = row["elapsed_minutes"]
    date = row["tournament_date"]

    adv_ranking = row["Ranking_2"]
    adv_ranking_points = row["Ranking_Points_2"]

    num_won_sets = 0
    num_lost_sets = 0
    num_won_games = 0
    num_lost_games = 0
    num_tie_break_wons = 0
    num_tie_break_lost = 0

    for set in row["score"].split(" "):
        try:
            games_0 = set.split("-")[0]
            games_1 = set.split("-")[1]

            if "(" in games_0:
                games_0 = games_0.split("(")[0]
                num_tie_break_lost += 1

            elif "(" in games_1:
                games_1 = games_1.split("(")[0]
                num_tie_break_wons += 1

            games_0 = int(games_0)
            games_1 = int(games_1)

            if games_0 > games_1:
                num_won_sets += 1
            elif games_0 < games_1:
                num_lost_sets += 1

            num_won_games += games_0
            num_lost_games += games_1
        except:
            if set not in ["ABD", "RET", "W/O"]:
                if verbose == 2:
                    print(set)
                else:
                    pass

    match_df = pd.DataFrame(
        {
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
            "num_tie_break_lost": [num_tie_break_lost],
        }
    )
    return match_df


def matches_info_norm(matches_info, current_date=""):
    # Normalize values
    tournament_surface = {"Clay": 0.0, "Carpet": 1 / 3, "Hard": 2 / 3, "Grass": 1.0}
    # nb sets won: max 3
    # nb sets lost: max 3
    # nb games won: max 100 (from experience - to be validated)
    # nb games lost: max 100 (from experience - to be validated)
    # nb tiebreaks won: max 100 (from experience - to be validated) -> not number of points but nb of tiebreaks ?
    # nb tiebreaks lost: max 100 (from experience - to be validated)
    # Ranking points max 16,950 from Djokovic's record -> 20,000
    # Ranking max 9,999
    # Num played minutes max 671 from Mahut/Isner's record -> 700
    # date: compute number of days since tournament date -> normalize by 365 -> if > 365 give up ?

    matches_info = matches_info.copy()
    matches_info["surface"] = matches_info["surface"].apply(
        lambda val: tournament_surface[val]
    )
    matches_info["num_won_sets"] = matches_info["num_won_sets"].apply(
        lambda val: val / 3
    )
    matches_info["num_lost_sets"] = matches_info["num_lost_sets"].apply(
        lambda val: val / 3
    )

    matches_info["date"] = matches_info["date"].apply(
        lambda val: get_days_difference(val, current_date) / 365
    )
    matches_info["num_played_minutes"] = matches_info["num_played_minutes"].apply(
        lambda val: val / 700
    )

    matches_info["adv_ranking"] = matches_info["adv_ranking"].apply(
        lambda val: np.log(val) / np.log(9999)
    )
    matches_info["adv_ranking_points"] = matches_info["adv_ranking_points"].apply(
        lambda val: val / 20000
    )

    matches_info["num_won_games"] = matches_info["num_won_games"].apply(
        lambda val: val / 100
    )
    matches_info["num_lost_games"] = matches_info["num_lost_games"].apply(
        lambda val: val / 100
    )
    matches_info["num_tie_break_wons"] = matches_info["num_tie_break_wons"].apply(
        lambda val: val / 3
    )
    matches_info["num_tie_break_lost"] = matches_info["num_tie_break_lost"].apply(
        lambda val: val / 3
    )

    return matches_info


def create_dataset(
    data_df, num_matches_difference=10, nb_kept_differences=10, randomize_indexes=False
):
    """
    Creates the match representation dataset
    :param data_df:
    :param num_matches_difference:
    :param nb_kept_differences:
    :return:
    """
    dataset = []
    for i in range(len(data_df)):
        current_row = data_df.iloc[i]
        current_player = current_row.ID_1
        sub_data_df = data_df.loc[data_df.ID_1 == current_player].iloc[: i - 1]
        if len(sub_data_df) > 0:
            sub_data_df = sub_data_df.reset_index(drop=True)

            kept_indexes = list(
                range(-min(len(sub_data_df), num_matches_difference), 0)
            )
            if randomize_indexes:
                kept_indexes = np.random.permutation(kept_indexes)
            kept_indexes = kept_indexes[:nb_kept_differences]
            sub_data_df = sub_data_df.iloc[kept_indexes]
            sub_data_df = sub_data_df.reset_index(drop=True)

            raw_matches_info = pd.concat(
                [get_match_info(sub_data_df.iloc[i]) for i in range(len(sub_data_df))],
                axis=0,
            )
            normalized_matches_info = matches_info_norm(
                raw_matches_info, current_date=current_row["tournament_date"]
            )
            dataset.append(normalized_matches_info)

    return pd.concat(dataset, axis=0)


def create_timeless_dataset(
    data_df,
    columns=[
        "surface",
        "result",
        "num_played_minutes",
        "adv_ranking",
        "adv_ranking_points",
        "num_won_sets",
        "num_lost_sets",
        "num_won_games",
        "num_lost_games",
        "num_tie_break_wons",
        "num_tie_break_lost",
    ],
):
    dataset = []
    for i in range(len(data_df)):
        raw_matches_info = get_match_info(data_df.iloc[i])
        dataset.append(raw_matches_info)
    dataset = pd.concat(dataset, axis=0)

    dataset = matches_info_norm(
        dataset, current_date=data_df["tournament_date"].values[-1]
    )
    dataset = dataset.drop(["date"], axis=1)
    return dataset[columns]
