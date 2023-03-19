import ast


def clean_missing_data(df):
    """
    Cleans rows of df with missing data or to few statistics to be useful
    :param df:
    :return:
    """

    df = df.dropna(axis=0)
    df = df.loc[df.Ranking_1 != 9999]
    df = df.loc[df.Ranking_1 != 0]
    df = df.loc[df.Ranking_2 != 9999]
    df = df.loc[df.Ranking_2 != 0]

    return df


def encode_data(df, mode="integer"):
    # Remove:
    #   - index
    #   - Unnamed: 0
    #   - Unnamed: 0.1
    #   - tournament
    #   - Name
    #   - ID
    #   - Birth Year => Age
    #   - Versus: % V against 2, last 5 matches
    #   - Matches

    # Refac:
    #   - Versus
    # Best way to do it ?
    #   - Birth Year
    #   - Last Tournament => Days since last tournament + result ?

    df_copy = df.copy()
    if mode == "integer":
        # Considered Variables:
        tournament_level = {"G": 0, "A": 1, "M": 2, "F": 3, "D": 4}
        tournament_surface = {"Clay": 0, "Carpet": 1, "Hard": 2, "Grass": 3}

        round = {
            "F": 0,
            "SF": 1,
            "QF": 2,
            "R16": 3,
            "R32": 4,
            "R64": 5,
            "R128": 6,
            "R256": 7,
            "RR": 8,
            "BR": 9,
            "ER": 10,
        }

        hand = {
            "R": -1,
            "L": 1,
            "A": 0,
            "U": 2,
            "nan": 2,
        }

    elif mode == "one_hot":
        # Considered Variables:
        tournament_level = {
            "G": [0, 0, 0, 1],
            "A": [0, 0, 1, 0],
            "M": [0, 1, 0, 0],
            "D": [1, 0, 0, 0],
        }

        tournament_surface = {
            "Clay": [1, 0, 0, 0],
            "Carpet": [0, 1, 0, 0],
            "Hard": [0, 0, 1, 0],
            "Grass": [0, 0, 0, 1],
        }

        round = {
            "F": [0, 0, 0, 0, 0, 0, 0, 0, 1],
            "SF": [0, 0, 0, 0, 0, 0, 0, 1, 0],
            "QF": [0, 0, 0, 0, 0, 0, 1, 0, 0],
            "R16": [0, 0, 0, 0, 0, 1, 0, 0, 0],
            "R32": [0, 0, 0, 0, 1, 0, 0, 0, 0],
            "R64": [0, 0, 0, 1, 0, 0, 0, 0, 0],
            "R128": [0, 0, 1, 0, 0, 0, 0, 0, 0],
            "R256": [0, 1, 0, 0, 0, 0, 0, 0, 0],
            "RR": [1, 0, 0, 0, 0, 0, 0, 0, 0],
        }

        hand = {
            "R": [1, 0, 0, 0],
            "L": [0, 1, 0, 0],
            "A": [0, 0, 1, 0],
            "U": [0, 0, 0, 1],
        }

    elif mode == "mixing":
        # Considered Variables:
        tournament_level = {"G": 0, "A": 1, "M": 2, "F": 3, "D": 4}
        tournament_surface = {
            "Clay": [1, 0, 0, 0],
            "Carpet": [0, 1, 0, 0],
            "Hard": [0, 0, 1, 0],
            "Grass": [0, 0, 0, 1],
        }

        round = {
            "F": 0,
            "SF": 1,
            "QF": 2,
            "R16": 3,
            "R32": 4,
            "R64": 5,
            "R128": 6,
            "R256": 7,
            "RR": 8,
            "BR": 9,
        }

        hand = {
            "R": [1, 0, 0, 0],
            "L": [0, 1, 0, 0],
            "A": [0, 0, 1, 0],
            "U": [0, 0, 0, 1],
        }

    for col in df_copy.columns:
        if "hand" in col.lower():
            df_copy[col] = df_copy.apply(lambda row: hand[str(row[col])], axis=1)
        elif "round" in col.lower():
            df_copy[col] = df_copy.apply(lambda row: round[row[col]], axis=1)
        elif "tournament_level" in col.lower():
            df_copy[col] = df_copy.apply(lambda row: tournament_level[row[col]], axis=1)
        elif "tournament_surface" in col.lower():
            df_copy[col] = df_copy.apply(
                lambda row: tournament_surface[row[col]], axis=1
            )
        else:
            pass

    return df_copy


def create_additional_features(df, features):
    df = df.copy()

    if "nb_match_versus" in features:
        df["nb_match_versus"] = df.apply(lambda row: len(row["Versus_1"]), axis=1)

    if "v_perc_versus" in features:
        df["v_perc_versus"] = df.apply(
            lambda row: [k[0] for k in row["Versus_1"]].count("V")
            / len([k[0] for k in row["Versus_1"]])
            if len(row["Versus_1"]) > 0
            else -1,
            axis=1,
        )

    if "diff_rank" in features:
        df["diff_rank"] = df.apply(
            lambda row: row["Ranking_2"] - row["Ranking_1"], axis=1
        )

    if "diff_rank_points" in features:
        df["diff_rank_points"] = df.apply(
            lambda row: row["Ranking_Points_2"] - row["Ranking_Points_1"], axis=1
        )

    return df
