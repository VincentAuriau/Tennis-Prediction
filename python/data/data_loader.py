import os
import re

import numpy as np
import pandas as pd

import player
import match


def create_player_profiles(df):
    players_db = {}
    for n_row, row in df.iterrows():
        pl = player.Player(name=(str(row["name_first"])+"."+str(row["name_last"])),
                           birthdate=row["dob"],
                           country=row["ioc"],
                           nb_id=row["player_id"],
                           hand=row["hand"],
                           height=row["height"])

        assert row["player_id"] not in players_db.keys()
        players_db[row["player_id"]] = pl
    return players_db

def read_matches_file(path_to_file):
    df_match = pd.read_csv(path_to_file)
    return df_match

def get_match_files(path_to_data_dir, match_type=["main_tour"]):
    main_atp_pattern = "atp_matches_(?P<year>\d+).csv"
    futures_pattern = "atp_matches_futures_(?P<year>\d+).csv"
    qual_chall_pattern = "atp_matches_qual_chall_(?P<year>\d+).csv"

    matches_data_file = {}

    for file in os.listdir(path_to_data_dir):
        regex_match = re.match(main_atp_pattern, file)
        if regex_match is not None:
            matches_data_file["filepath"] = matches_data_file.get("filepath", []) + [os.path.join(path_to_data_dir,
                                                                                                  file)]
            matches_data_file["match_type"] = matches_data_file.get("match_type", []) + ["main_tour"]
            match_dict = regex_match.groupdict()
            for key, value in match_dict.items():
                matches_data_file[key] = matches_data_file.get(key, []) + [value]
    return pd.DataFrame(matches_data_file)

def load_match_data_from_path(players_db, path_to_file):
    match_df = pd.read_csv(path_to_file)

    matches_data = []
    for n_row, row in match_df.iterrows():
        m_winner = players_db[row["winner_id"]]
        m_loser = players_db[row["loser_id"]]
        m_tournament = row["tourney_name"]
        m_surface = row["surface"]

        match_o = match.Match(winner=m_winner, loser=m_loser, tournament=m_tournament, surface=m_surface)
        match_o.instantiate_from_data_row(row)
        match_data, w_data, l_data = match_o.get_predictable_data_and_update_players_stats()

        to_1 = {}
        to_2 = {}
        for col in w_data.columns:
            to_1[col] = col + "_1"
            to_2[col] = col + "_2"

        concat_1 = pd.concat([w_data.copy().rename(to_1, axis=1), l_data.copy().rename(to_1, axis=1)], axis=0)
        concat_2 = pd.concat([l_data.copy().rename(to_2, axis=1), w_data.copy().rename(to_2, axis=1)], axis=0)

        final_df = pd.concat([pd.concat([match_data]*2, axis=0), concat_1, concat_2], axis=1)
        final_df["Winner"] = [0, 1]
        matches_data.append(final_df)
    return pd.concat(matches_data, axis=0)

def load_matches_data():

    path_to_data = "submodules/tennis_atp"
    data_files = get_match_files(path_to_data)

    df_players = pd.read_csv(os.path.join(path_to_data, 'atp_players.csv'), header=0,
                            encoding="ISO-8859-1")
    players_db = create_player_profiles(df_players)
    data_years = data_files.year.astype("uint32") # to change when handling different type of tournament (qualifiers, main, etc...)

    data_per_year = []
    for year in np.sort(data_years.values):
        print("+---------+---------+")
        print("  Loading Data ...  ")
        print("Currently year:", year)
        print("+---------+---------+")
        filepath = data_files.loc[data_files.year == str(year)]["filepath"].values[0]
        df_year = load_match_data_from_path(players_db, filepath)
        data_per_year.append(df_year)

    return pd.concat(data_per_year, axis=0)

def data_loader():
    # Encodes data
    # returns X, y, df
    return None


# players_db = create_player_profiles(df_players)
# print(players_db)
df = load_matches_data()
df.to_csv('all_data.csv')
df = pd.read_csv('all_data.csv')
df.iloc[-1000:].to_csv('sub_data.csv')
df = pd.read_csv('sub_data.csv')
print(df.head())
