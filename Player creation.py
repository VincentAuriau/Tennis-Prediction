import pandas as pd
import Player

df_players = pd.read_csv('Data/atp_players.csv', header=None, names=[1, 2, 3, 4, 5, 6], encoding="ISO-8859-1")
df_matches_2012 = pd.read_csv('Data/atp_matches_2012.csv')
df_matches_2012 = df_matches_2012.sort_values(by='tourney_date').reset_index()
print(df_matches_2012)

list_players_2012 = {}
for row in range(len(df_matches_2012)):
    id_winner = df_matches_2012['winner_id'][row]
    id_loser = df_matches_2012['loser_id'][row]
    height_winner = df_matches_2012['winner_ht'][row]
    hand_winner = df_matches_2012['winner_hand'][row]
    height_loser = df_matches_2012['loser_ht'][row]
    hand_loser = df_matches_2012['loser_hand'][row]
    list_players_2012[id_winner] = [height_winner, hand_winner]
    list_players_2012[id_loser] = [height_loser, hand_loser]

players_list = []

for row in range(len(df_players)):
    id_nb = df_players[1][row]
    if id_nb in list_players_2012.keys():
        name = str(df_players[2][row]) + ' ' + str(df_players[3][row])
        born_year = str(df_players[5][row])[:4]
        country = str(df_players[6][row])
        player = Player.Player(name, born_year, country, id_nb)
        hand = list_players_2012[id_nb][1]
        height = list_players_2012[id_nb][0]
        if hand != 'nan'and hand == hand:
            player.hand = list_players_2012[id_nb][1]
        if height != 'nan' and height == height:
            player.height = list_players_2012[id_nb][0]
        players_list.append(player)

for row in range(len(df_matches_2012)):
    id_winner = df_matches_2012['winner_id'][row]
    id_loser = df_matches_2012['loser_id'][row]
    tournament_date = str(df_matches_2012['tourney_date'][row])
    sets_number = df_matches_2012['score'][row].count("-")
    surface = df_matches_2012['surface'][row]

    w_ace = df_matches_2012['w_ace'][row]
    w_svpt = df_matches_2012['w_svpt'][row]
    w_df = df_matches_2012['w_df'][row]
    w_1stwon = df_matches_2012['w_1stWon'][row]
    w_2ndwon = df_matches_2012['w_2ndWon'][row]
    l_ace = df_matches_2012['l_ace'][row]
    l_svpt = df_matches_2012['l_svpt'][row]
    l_df = df_matches_2012['l_df'][row]
    l_1stwon = df_matches_2012['l_1stWon'][row]
    l_2ndwon = df_matches_2012['l_2ndWon'][row]


    print('sets number', sets_number)
    for player in players_list:
        if player.id == id_winner:
            player.add_victory(id_loser)
            player.last_tournament_date = tournament_date
            player.update_fatigue(tournament_date, sets_number)
            player.update_surface_victory_percentage(surface, 'V')
            if w_svpt == w_svpt and w_ace == w_ace:
                player.update_ace_percentage(w_ace, w_svpt)
            if w_svpt == 0:
                print('div by 0', row)
            if w_svpt == w_svpt and w_df == w_df:
                player.update_doublefault_percentage(w_df, w_svpt)
            if w_svpt == w_svpt and w_1stwon == w_1stwon and w_2ndwon == w_2ndwon:
                player.update_winning_on_1st_serve_percentage(w_1stwon, w_svpt)
                player.update_winning_on_2nd_serve_percentage(w_2ndwon, w_svpt)

        elif player.id == id_loser:
            player.add_defeat(id_winner)
            player.last_tournament_date = tournament_date
            player.update_fatigue(tournament_date, sets_number)
            player.update_surface_victory_percentage(surface, 'D')
            if l_svpt == l_svpt and l_ace == l_ace:
                player.update_ace_percentage(l_ace, l_svpt)
            if l_svpt == l_svpt and l_df == l_df:
                player.update_doublefault_percentage(l_df, l_svpt)
            if l_svpt == l_svpt and l_1stwon == l_1stwon and l_2ndwon == l_2ndwon:
                player.update_winning_on_1st_serve_percentage(l_1stwon, l_svpt)
                player.update_winning_on_2nd_serve_percentage(l_2ndwon, l_svpt)

print(players_list)
for player in players_list:
    print(player)
    print('          Last Matches :  ', player.last_matches, ' *** Victory Percentage : ', player.victory_percentage,
          '%')
    print('           *** Ace Percentage : ', player.ace_percentage, '%')
    print('           *** Double Fault Percentage : ', player.doublefault_percentage, '%')
    print('           *** Serve Point Won Percentage : ', player.overall_win_on_serve_percentage, '%')
    if player.id == 104745 or player.id == 104932:
        print(player.matches)
