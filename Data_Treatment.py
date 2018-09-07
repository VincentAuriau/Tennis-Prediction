import pickle
import pandas as pd

with open('Data_2012', 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    data_not_treated = my_unpickler.load()

print(data_not_treated[0])

data_treated = []

# 69 different tournaments
# 6 different levels
# 4 different surfaces
# 1 different round which is '' -> ISSUE TO FIX WITH THE ROUNDS

max_tournament = 0
tournaments_already_visited = {}
level_dict = {'A': 1, 'C': 2, 'D': 3, 'F': 4, 'G': 5, 'M': 6}
surface_dict = {'Hard': 4, 'Grass': 3, 'Clay': 1, 'Carpet': 2}

for match_not_treated in data_not_treated:
    match_data_treated = []

    # Match
    tournament = match_not_treated[0][0]

    if tournament in tournaments_already_visited.keys():
        match_data_treated.append(tournaments_already_visited[tournament])
    elif 'Davis' in tournament:
        match_data_treated.append(69)
    else:
        max_tournament += 1
        tournaments_already_visited[tournament] = max_tournament
        match_data_treated.append(tournaments_already_visited[tournament])

    level = match_not_treated[0][1]
    match_data_treated.append(level_dict[level])

    surface = match_not_treated[0][2]
    match_data_treated.append(surface_dict[surface])

    print(match_data_treated)

    # Players

    # Ranking
    rankings = [match_not_treated[1][2], match_not_treated[2][2]]
    # print(rankings)

    # Ranking points
    points = [match_not_treated[1][3], match_not_treated[2][3]]
    print(points)

    # Hand
    hands = []
    for i in range(2):
        if match_not_treated[i + 1][6] == 'L':
            hands += [0]
        else:
            hands += [1]
    # print(hands)

    # Height
    heights = [match_not_treated[1][8], match_not_treated[2][8]]
    # print(heights)

    # Percentages
    percentages = [match_not_treated[1][14], match_not_treated[2][14]]
    percentages += [match_not_treated[1][14 + surface_dict[surface]], match_not_treated[2][14 + surface_dict[surface]]]

    for i in range(8):
        percentages += [match_not_treated[1][i + 19], match_not_treated[2][i + 19]]
    print(percentages)

    # Fatigue
    fatigues = [match_not_treated[1][27], match_not_treated[2][27]]
    # print(fatigues)

    # Age
    year = 2012
    ages = [2012 - int(match_not_treated[1][4]), 2012 - int(match_not_treated[2][4])]
    # print(ages)

    # Last Matches
    last_matches_w = match_not_treated[1][9][-5:]
    # print(last_matches_w)
    last_matches_w_win_percentage = last_matches_w.count('V') * 20
    # print(last_matches_w_win_percentage)
    last_matches_l = match_not_treated[2][9][-5:]
    last_matches_l_win_percentage = last_matches_l.count('V') * 20

    # Last Matches Surface
    # print(surface_dict[surface])
    last_matches_w_surface = match_not_treated[1][9+surface_dict[surface]][-5:]
    # print(last_matches_w_surface)
    last_matches_w_win_percentage_surface = last_matches_w_surface.count('V') * 20
    # print(last_matches_w_win_percentage_surface)
    last_matches_l_surface = match_not_treated[2][9+surface_dict[surface]][-5:]
    last_matches_l_win_percentage_surface = last_matches_l_surface.count('V') * 20

