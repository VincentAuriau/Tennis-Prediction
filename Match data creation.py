import Player
import Match
import pickle
import pandas as pd

df_matches_2012 = pd.read_csv('Data/atp_matches_2012.csv')
df_matches_2012 = df_matches_2012.sort_values(by='tourney_date').reset_index()
print(df_matches_2012)

whole_data = []

with open('Players_2012_profiles', 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    players_dict = my_unpickler.load()

for row in range(len(df_matches_2012)):
    tournament_name = df_matches_2012['tourney_name'][row]
    id_winner = df_matches_2012['winner_id'][row]
    id_loser = df_matches_2012['loser_id'][row]
    tournament_date = str(df_matches_2012['tourney_date'][row])
    surface = df_matches_2012['surface'][row]
    tournament_level = df_matches_2012['tourney_level'][row]
    round = df_matches_2012['round'][row]

    winner = players_dict[id_winner]
    loser = players_dict[id_loser]
    winner_rank = df_matches_2012['winner_rank'][row]
    winner_rank_points = df_matches_2012['winner_rank_points'][row]
    loser_rank = df_matches_2012['loser_rank'][row]
    loser_rank_points = df_matches_2012['loser_rank_points'][row]
    winner.ranking = winner_rank
    winner.ranking_points = winner_rank_points
    loser.ranking = loser_rank
    loser.ranking_points = loser_rank_points

    match = Match.Match(winner, loser, tournament_name, tournament_date)
    match.surface = surface
    match.tournament_level = tournament_level
    match.round = round

    print(match.get_data()[1][:2], match.get_data()[1][-2])

    score = df_matches_2012['score'][row]
    if score == score and type(score) == str:
        sets_number = score.count('-')

    w_ace = df_matches_2012['w_ace'][row]
    w_svpt = df_matches_2012['w_svpt'][row]
    w_df = df_matches_2012['w_df'][row]
    w_1stwon = df_matches_2012['w_1stWon'][row]
    w_2ndwon = df_matches_2012['w_2ndWon'][row]
    w_1stIn = df_matches_2012['w_1stIn'][row]
    w_bp_Saved = df_matches_2012['w_bpSaved'][row]
    w_bp_Faced = df_matches_2012['w_bpFaced'][row]
    w_SvGms = df_matches_2012['w_SvGms'][row]

    l_ace = df_matches_2012['l_ace'][row]
    l_svpt = df_matches_2012['l_svpt'][row]
    l_df = df_matches_2012['l_df'][row]
    l_1stwon = df_matches_2012['l_1stWon'][row]
    l_2ndwon = df_matches_2012['l_2ndWon'][row]
    l_1stIn = df_matches_2012['l_1stIn'][row]
    l_bp_Saved = df_matches_2012['l_bpSaved'][row]
    l_bp_Faced = df_matches_2012['l_bpFaced'][row]
    l_SvGms = df_matches_2012['l_SvGms'][row]

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

    whole_data += [match.get_data()]

print(whole_data[0])

with open('Data_2012', 'wb') as file:
    my_pickler = pickle.Pickler(file)
    my_pickler.dump(whole_data)
