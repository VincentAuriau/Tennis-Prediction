import ast
import numpy as np
import pandas as pd
import tqdm

from history_modeling.match_representation import (
    create_timeless_dataset,
    get_match_info,
)


def clean_missing_data(df):
    """
    Cleans rows of df with missing data or to few statistics to be useful
    :param df:
    :return:
    """
    print("Length df before cleaning:", len(df))
    df = df.dropna(axis=0)
    print("after dropna", len(df))
    # df = df.loc[df.Ranking_1 != 9999]
    df = df.loc[df.Ranking_1 != 0]
    # df = df.loc[df.Ranking_2 != 9999]
    df = df.loc[df.Ranking_2 != 0]

    return df


def complete_missing_data(df, *args):
    for column, value in args:
        df[column].fillna(value, inplace=True)

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
        tournament_level = {"G": 0, "A": 1, "M": 2, "F": 3, "D": 4, "C": 5}
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
            "Q1": 11,
            "Q2": 12,
            "Q3": 13,
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
            "G": [0, 0, 0, 1, 0],
            "A": [0, 0, 1, 0, 0],
            "M": [0, 1, 0, 0, 0],
            "D": [1, 0, 0, 0, 0],
            "C": [0, 0, 0, 0, 1],
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
        tournament_level = {"G": 0, "A": 1, "M": 2, "F": 3, "D": 4, "C": 5}
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
        df["nb_match_versus"] = df.apply(
            lambda row: len([k[0] for k in ast.literal_eval(row["Versus_1"])]), axis=1
        )

    if "v_perc_versus" in features:
        df["v_perc_versus"] = df.apply(
            lambda row: [k[0] for k in ast.literal_eval(row["Versus_1"])].count("V")
            / len([k[0] for k in ast.literal_eval(row["Versus_1"])])
            if len([k[0] for k in ast.literal_eval(row["Versus_1"])]) > 0
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


def create_encoded_history(df, encoder, num_matches, completing_value=0):
    df = df.copy()
    history = {
        "id": [],
        "ID_1": [],
        "ID_2": [],
        "history_1": [],
        "history_2": [],
    }

    for n_row, row in tqdm.tqdm(df.iterrows(), total=len(df)):
        try:
            matches_history_1 = ast.literal_eval(row["Matches_1"])[-num_matches:]
        except:
            with open("error.txt", "w") as file:
                file.write(str(row["Matches_1"]))
            matches_history_1 = ast.literal_eval(row["Matches_1"])[-num_matches:]

        matches_history_1 = [_[1] for _ in matches_history_1]

        df_history = df.loc[df.id.isin(matches_history_1)].loc[df.ID_1 == row.ID_1]

        if len(df_history) > 0:
            # df_history = create_timeless_dataset(df_history)
            # encoded_history_1 = encoder.predict(df_history)
            encoded_history_1, df_history = encoder.predict(
                df_history, transform_data=True
            )

            if encoded_history_1.shape[0] < num_matches:
                encoded_history_1 = np.concatenate(
                    [
                        np.ones(
                            (
                                num_matches - encoded_history_1.shape[0],
                                encoded_history_1.shape[1],
                            )
                        )
                        * completing_value,
                        encoded_history_1,
                    ],
                    axis=0,
                )
        else:
            encoded_history_1 = (
                np.ones((num_matches, encoder.output_shape)) * completing_value
            )

        matches_history_2 = ast.literal_eval(row["Matches_2"])[-num_matches:]
        matches_history_2 = [_[1] for _ in matches_history_2]

        df_history = df.loc[df.id.isin(matches_history_2)].loc[df.ID_1 == row.ID_2]

        if len(df_history) > 0:
            # df_history = create_timeless_dataset(df_history)
            encoded_history_2, df_history = encoder.predict(
                df_history, transform_data=True
            )

            if encoded_history_2.shape[0] < num_matches:
                encoded_history_2 = np.concatenate(
                    [
                        np.ones(
                            (
                                num_matches - encoded_history_2.shape[0],
                                encoded_history_2.shape[1],
                            )
                        )
                        * completing_value,
                        encoded_history_2,
                    ],
                    axis=0,
                )
        else:
            encoded_history_2 = (
                np.ones((num_matches, encoder.output_shape)) * completing_value
            )

        history["id"].append(row.id)
        history["ID_1"].append(row.ID_1)
        history["ID_2"].append(row.ID_2)

        history["history_1"].append(encoded_history_1)
        history["history_2"].append(encoded_history_2)

        if n_row < 100 and len(df_history) > 0:
            row.to_csv("row.csv")
            df_history.to_csv("df_history.csv")
            np.save("encoded_history.npy", encoded_history_2)
    return pd.DataFrame(history)
