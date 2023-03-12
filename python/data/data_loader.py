import os
import pickle
import re
from ast import literal_eval

import numpy as np
import pandas as pd

import data.player as player
import data.match as match


def create_player_profiles(df):
    """
    Creates database of players from df containing list of players
    :param df: pandas.DataFrame corresponding to atp_players.csv
    :return: databaser of player.Players objects
    """
    players_db = {}
    for n_row, row in df.iterrows():
        pl = player.Player(
            name=(str(row["name_first"]) + "." + str(row["name_last"])),
            birthdate=row["dob"],
            country=row["ioc"],
            nb_id=row["player_id"],
            hand=row["hand"],
            height=row["height"],
        )

        assert row["player_id"] not in players_db.keys()
        players_db[row["player_id"]] = pl
    return players_db


def read_matches_file(path_to_file):
    """
    Opens a csv file with matches
    :param path_to_file:
    :return: corresponding df
    """
    df_match = pd.read_csv(path_to_file)
    return df_match


def get_match_files(path_to_data_dir, match_type=["main_atp"]):
    """
    Lists the available csv containing matches
    :param path_to_data_dir: path to directory with all files
    :param match_type: matches we want to retrieve list of elements among ["main_atp", "futures", "qualifying_challengers"]
    :return:
    """
    main_atp_pattern = "atp_matches_(?P<year>\d+).csv"
    futures_pattern = "atp_matches_futures_(?P<year>\d+).csv"
    qual_chall_pattern = "atp_matches_qual_chall_(?P<year>\d+).csv"

    matches_data_file = {}

    for file in os.listdir(path_to_data_dir):
        if "main_atp" in match_type:
            regex_match = re.match(main_atp_pattern, file)
            if regex_match is not None:
                matches_data_file["filepath"] = matches_data_file.get(
                    "filepath", []
                ) + [os.path.join(path_to_data_dir, file)]
                matches_data_file["match_type"] = matches_data_file.get(
                    "match_type", []
                ) + ["main_tour"]
                match_dict = regex_match.groupdict()
                for key, value in match_dict.items():
                    matches_data_file[key] = matches_data_file.get(key, []) + [value]
        if "futures" in match_type:
            regex_match = re.match(futures_pattern, file)
            if regex_match is not None:
                matches_data_file["filepath"] = matches_data_file.get(
                    "filepath", []
                ) + [os.path.join(path_to_data_dir, file)]
                matches_data_file["match_type"] = matches_data_file.get(
                    "match_type", []
                ) + ["main_tour"]
                match_dict = regex_match.groupdict()
                for key, value in match_dict.items():
                    matches_data_file[key] = matches_data_file.get(key, []) + [value]
        if "qualifying_challengers" in match_type:
            regex_match = re.match(qual_chall_pattern, file)
            if regex_match is not None:
                matches_data_file["filepath"] = matches_data_file.get(
                    "filepath", []
                ) + [os.path.join(path_to_data_dir, file)]
                matches_data_file["match_type"] = matches_data_file.get(
                    "match_type", []
                ) + ["main_tour"]
                match_dict = regex_match.groupdict()
                for key, value in match_dict.items():
                    matches_data_file[key] = matches_data_file.get(key, []) + [value]
    return pd.DataFrame(matches_data_file)


def load_match_data_from_path(
    players_db, path_to_matchs_file, get_match_statistics=False
):
    """
    Loads file from path and creates the matches data while updating players databaser
    :param players_db:
    :param path_to_matchs_file:
    :return:
    """

    def extract_file_id(file_path):

        file_id = path_to_matchs_file.split("/")[-1].split(".")[0]
        if "\\" in file_id:
            file_id = file_id.split("\\")[1]

        return file_id

    match_df = pd.read_csv(path_to_matchs_file)
    match_df["match_id"] = match_df.apply(
        lambda row: extract_file_id(path_to_matchs_file)
        + "_"
        + str(row.name),
        axis=1,
    )

    matches_data = []
    for n_row, row in match_df.iterrows():
        m_winner = players_db[row["winner_id"]]
        m_loser = players_db[row["loser_id"]]
        m_tournament = row["tourney_name"]
        m_surface = row["surface"]

        match_o = match.Match(
            winner=m_winner, loser=m_loser, tournament=m_tournament, surface=m_surface
        )
        match_o.instantiate_from_data_row(row)
        (
            match_data,
            w_data,
            l_data,
        ) = match_o.get_prior_data_and_update_players_stats()

        match_data["match_id"] = row["match_id"]

        to_1 = {}
        to_2 = {}
        for col in w_data.columns:
            to_1[col] = col + "_1"
            to_2[col] = col + "_2"

        concat_1 = pd.concat(
            [w_data.copy().rename(to_1, axis=1), l_data.copy().rename(to_1, axis=1)],
            axis=0,
        )
        concat_2 = pd.concat(
            [l_data.copy().rename(to_2, axis=1), w_data.copy().rename(to_2, axis=1)],
            axis=0,
        )

        final_df = pd.concat(
            [pd.concat([match_data] * 2, axis=0), concat_1, concat_2], axis=1
        )
        final_df["Winner"] = [0, 1]

        if get_match_statistics:
            (
                match_stats,
                w_mstats,
                l_mstats,
            ) = match_o.get_match_data_results_statistics()
            ms_to_1 = {}
            ms_to_2 = {}
            for col in w_mstats.columns:
                ms_to_1[col] = col + "_1"
                ms_to_2[col] = col + "_2"

            ms_concat_1 = pd.concat(
                [
                    w_mstats.copy().rename(ms_to_1, axis=1),
                    l_mstats.copy().rename(ms_to_1, axis=1),
                ],
                axis=0,
            )
            ms_concat_2 = pd.concat(
                [
                    l_mstats.copy().rename(ms_to_2, axis=1),
                    w_mstats.copy().rename(ms_to_2, axis=1),
                ],
                axis=0,
            )
            match_stats_df = pd.concat(
                [pd.concat([match_stats] * 2, axis=0), ms_concat_1, ms_concat_2], axis=1
            )
            final_df = pd.concat([final_df, match_stats_df], axis=1)

        matches_data.append(final_df)

    matches_data = pd.concat(matches_data, axis=0)
    return matches_data


def matches_data_loader(
    keep_values_from_year=1990,
    path_to_data="submodules/tennis_atp",
    path_to_cache="/cache",
    flush_cache=True,
    get_match_statistics=False,
    get_reversed_match_data=False,
):
    """
    Loads all matches data
    :return:
    """

    # Check if data already in cache
    if os.path.exists(os.path.join(path_to_cache, "players_db")):
        players_db_cached = True
    else:
        players_db_cached = False

    if os.path.exists(
        os.path.join(path_to_cache, f"matches_data_{keep_values_from_year}.csv")
    ):
        matches_data_cached = True
    else:
        matches_data_cached = False

    if not players_db_cached or flush_cache:
        df_players = pd.read_csv(
            os.path.join(path_to_data, "atp_players.csv"),
            header=0,
            encoding="ISO-8859-1",
        )
        players_db = create_player_profiles(df_players)
        with open(os.path.join(path_to_cache, "players_db"), "wb") as file:
            pickle.dump(players_db, file, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(os.path.join(path_to_cache, "players_db"), "rb") as file:
            players_db = pickle.load(file)

    if not matches_data_cached or flush_cache:
        data_files = get_match_files(path_to_data)
        data_years = data_files.year.astype(
            "uint32"
        )  # to change when handling different type of tournament (qualifiers, main, etc...)

        data_per_year = []
        for year in np.sort(data_years.values):
            print("+---------+---------+")
            print("  Year %i  " % year)
            if year >= keep_values_from_year:
                print("Updating players statistics & saving matches data")
            else:
                print("Only updating players statistics")
            print("+---------+---------+")
            filepath = data_files.loc[data_files.year == str(year)]["filepath"].values[
                0
            ]
            df_year = load_match_data_from_path(
                players_db, filepath, get_match_statistics=get_match_statistics
            )
            df_year["tournament_year"] = year
            if year >= keep_values_from_year:
                data_per_year.append(df_year)

                df_year.to_csv(
                    os.path.join(path_to_cache, f"matches_data_{year}.csv"),
                    sep=";",
                    index=False,
                )

        data_matches = pd.concat(data_per_year, axis=0)
        """
        data_matches.to_csv(
            os.path.join(path_to_cache, "matches_data.csv"), sep=";", index=False
        )
        """
    else:
        years = []
        file_pattern = "matches_data_(?P<year>\d+).csv"
        for file in os.listdir(path_to_cache):
            regex_match = re.match(file_pattern, file)
            if regex_match is not None:
                years.append(int(regex_match["year"]))

        data_per_year = []
        for year in np.sort(years):
            if year >= keep_values_from_year:
                df_year = pd.read_csv(
                    os.path.join(path_to_cache, f"matches_data_{year}.csv")
                )
                data_per_year.append(df_year)

        data_matches = pd.concat(data_per_year, axis=0)
        data_matches = data_matches.reset_index()
        """
        data_matches = pd.read_csv(
            os.path.join(path_to_cache, "matches_data.csv"), sep=";"
        )
        """
    if get_reversed_match_data:
        return data_matches
    else:
        return data_matches.iloc[::2]


def clean_missing_data(df):
    """
    Cleans rows of df with missing data or to few statistics to be useful
    :param df:
    :return:
    """

    df.dropna(axis=0)
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

    df_copy = df
    if mode == "integer":
        # Considered Variables:
        tournament_level = {"G": 0, "A": 1, "M": 2, "F": 3, "D": 4}

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
    print(df_copy.columns)
    for col in df_copy.columns:
        print("col", col)
        if "hand" in col.lower():
            df_copy[col] = df_copy.apply(lambda row: hand[str(row[col])], axis=1)
        elif "round" in col.lower():
            df_copy[col] = df_copy.apply(lambda row: round[row[col]], axis=1)
        elif "tournament_level" in col.lower():
            df_copy[col] = df_copy.apply(lambda row: tournament_level[row[col]], axis=1)
        else:
            print(col)

    def get_versus_1(row):
        vs_1 = row["Versus_1"]
        if isinstance(vs_1, str):
            try:
                vs_1 = literal_eval(vs_1)
            except:
                raise ValueError("Err_OR")
        return vs_1.get(row["ID_2"], [])

    print("Analyzing versus 1")
    df_copy["Versus_1"] = df_copy.apply(lambda row: get_versus_1(row), axis=1)
    df_copy["Versus_2"] = df_copy.apply(
        lambda row: literal_eval(row["Versus_2"]).get(row["ID_1"], []), axis=1
    )

    df_copy["nb_match_versus"] = df_copy.apply(lambda row: len(row["Versus_1"]), axis=1)
    df_copy["v_perc_versus"] = df_copy.apply(
        lambda row: row["Versus_1"].count("V") / len(row["Versus_1"])
        if len(row["Versus_1"]) > 0
        else -1,
        axis=1,
    )
    # df_copy["v_perc_versus_2"] = df_copy.apply(lambda row: row["Versus_2"].count("V") / len(row["Versus_2"]) if len(row["Versus_2"]) > 0 else -1, axis=1)

    return df_copy
