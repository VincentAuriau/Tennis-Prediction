import pickle
import sys
sys.path.append('../')
from Player import Player

import numpy as np
import pandas as pd

work_IDs = np.load('IDs_2019.npy')
print(len(work_IDs))

with open('2019_players', 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    players_dict = my_unpickler.load()


print(players_dict)
num_matches_analyed = 0

for year in range(1980, 2018):
    print('YEAR:', year)
    df_matches_year = pd.read_csv('../Data/atp_matches_%i.csv' % year)
    for id, row in df_matches_year.iterrows():
        num_matches_analyed += 1
        id_winner = row['winner_id']
        id_loser = row['loser_id']
        tournament_date = str(row['tourney_date'])
        score = row['score']
        if score == score and type(score) == str:
            sets_number = score.count('-')
        else:
            sets_number = -1
        surface = row['surface']

        w_ace = row['w_ace']
        w_svpt = row['w_svpt']
        w_df = row['w_df']
        w_1stwon = row['w_1stWon']
        w_2ndwon = row['w_2ndWon']
        w_1stIn = row['w_1stIn']
        w_bp_Saved = row['w_bpSaved']
        w_bp_Faced = row['w_bpFaced']
        w_SvGms = row['w_SvGms']

        l_ace = row['l_ace']
        l_svpt = row['l_svpt']
        l_df = row['l_df']
        l_1stwon = row['l_1stWon']
        l_2ndwon = row['l_2ndWon']
        l_1stIn = row['l_1stIn']
        l_bp_Saved = row['l_bpSaved']
        l_bp_Faced = row['l_bpFaced']
        l_SvGms = row['l_SvGms']


        # Update Player data :)
        winner = players_dict.get(id_winner, None)
        loser = players_dict.get(id_loser, None)

        if winner is not None:

            winner.add_victory(id_loser)
            winner.last_tournament_date = tournament_date
            winner.update_fatigue(tournament_date, sets_number)
            winner.update_surface_victory_percentage(surface, 'V')
            if w_svpt == w_svpt and w_ace == w_ace:
                winner.update_ace_percentage(w_ace, w_svpt)
            if w_svpt == 0:
                print('div by 0', row)
            if w_svpt == w_svpt and w_df == w_df:
                winner.update_doublefault_percentage(w_df, w_svpt)
            if w_svpt == w_svpt and w_1stwon == w_1stwon and w_2ndwon == w_2ndwon:
                winner.update_winning_on_1st_serve_percentage(w_1stwon, w_svpt)
                winner.update_winning_on_2nd_serve_percentage(w_2ndwon, w_svpt)
            if w_svpt == w_svpt and w_1stIn == w_1stIn:
                winner.update_first_serve_success_percentage(w_1stIn, w_svpt)
            if w_bp_Faced == w_bp_Faced and w_bp_Saved == w_bp_Saved and w_SvGms == w_SvGms:
                winner.update_breakpoint_faced_and_savec(w_bp_Faced, w_bp_Saved, w_SvGms)

        if loser is not None:
            loser.add_defeat(id_winner)
            loser.last_tournament_date = tournament_date
            loser.update_fatigue(tournament_date, sets_number)
            loser.update_surface_victory_percentage(surface, 'D')
            if l_svpt == l_svpt and l_ace == l_ace:
                loser.update_ace_percentage(l_ace, l_svpt)
            if l_svpt == l_svpt and l_df == l_df:
                loser.update_doublefault_percentage(l_df, l_svpt)
            if l_svpt == l_svpt and l_1stwon == l_1stwon and l_2ndwon == l_2ndwon:
                loser.update_winning_on_1st_serve_percentage(l_1stwon, l_svpt)
                loser.update_winning_on_2nd_serve_percentage(l_2ndwon, l_svpt)
            if l_svpt == l_svpt and l_1stIn == l_1stIn:
                loser.update_first_serve_success_percentage(l_1stIn, l_svpt)
            if l_bp_Faced == l_bp_Faced and l_bp_Saved == l_bp_Saved and l_SvGms == l_SvGms:
                loser.update_breakpoint_faced_and_savec(l_bp_Faced, l_bp_Saved, l_SvGms)

print('NUMBER OF MATCHES ANALYZED:', num_matches_analyed)
print('NUMBER OF PLAYERS:', len(players_dict.keys()))

with open('2019_players_updated', 'wb') as file:
    my_pickler = pickle.Pickler(file)
    my_pickler.dump(players_dict)

