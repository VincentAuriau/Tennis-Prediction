import pickle
import pandas as pd
import random

with open('Data_2012', 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    data_not_treated = my_unpickler.load()

print(data_not_treated[0])

data_treated = []

# 69 different tournaments
# 6 different levels
# 4 different surfaces
# 1 different round which is '' -> ISSUE TO FIX WITH THE ROUNDS

min_tournament = 0
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
        min_tournament += 1
        tournaments_already_visited[tournament] = min_tournament
        match_data_treated.append(tournaments_already_visited[tournament])

    level = match_not_treated[0][1]
    match_data_treated.append(level_dict[level])

    surface = match_not_treated[0][2]
    match_data_treated.append(surface_dict[surface])

    # print(match_data_treated)

    for player in range(1, 3):

        # Players

        # Ranking
        ranking = match_not_treated[player][2]
        # print(ranking)

        # Ranking points
        points = match_not_treated[player][3]
        print(points)

        # Hand
        if match_not_treated[player][6] == 'L':
            hand = 0
        else:
            hand = 1
        # print(hand)

        # Height
        height = match_not_treated[player][8]
        # print(heights)

        # Percentages
        percentages = [match_not_treated[player][14]]
        percentages += [match_not_treated[player][14 + surface_dict[surface]]]

        for i in range(8):
            percentages += [match_not_treated[player][i + 19]]
        # print(percentages)

        # Fatigue
        fatigue = match_not_treated[player][27]
        # print(fatigues)

        # Age
        year = 2012
        if match_not_treated[player][4] != 'nan' and match_not_treated[player][4] == match_not_treated[player][4]:
            age = 2012 - int(match_not_treated[player][4])
        else:
            age = 0

        # Last Matches
        matches = match_not_treated[player][9]
        last_matches = matches[-min(5, len(matches)):]
        # print(last_matches_w)
        last_matches_win_percentage = last_matches.count('V') * (100 / len(last_matches))
        # print(last_matches_w_win_percentage)

        # Last Matches Surface
        # print(surface_dict[surface])
        matches_surface = match_not_treated[player][9+surface_dict[surface]]
        last_matches_surface = matches_surface[-min(5, len(matches)):]
        # print(last_matches_w_surface)
        last_matches_win_percentage_surface = last_matches_surface.count('V') * (100 / len(last_matches_surface))
        # print(last_matches_w_win_percentage_surface)
        last_matches_surface = last_matches_win_percentage_surface

        # Matches agains each other
        results_actual_against_other = match_not_treated[player][5][match_not_treated[player % 2 + 1][1]]
        print(results_actual_against_other)
        win_percentage_actual_over_other = results_actual_against_other.count('V') / \
                                           len(results_actual_against_other) * 100

        print(win_percentage_actual_over_other)

        player_data_treated = [ranking, points, hand, height, fatigue, age, percentages, last_matches_win_percentage,
                               last_matches_surface, win_percentage_actual_over_other]

        match_data_treated += [player_data_treated]

    print(match_data_treated)
    data_treated += [match_data_treated]

print(data_treated)


def percentage_treatment(percentage_list):
    return_list = []
    for percentage in percentage_list:
        return_list.append(percentage * 0.01)
    return return_list


def float_treatment(floated, maxi, mini):
    return (2 / (maxi - mini)) * floated - ((maxi + mini) / (maxi - mini))


def extrema_determination(list_position):
    global data_treated
    maxi = data_treated[0][3][list_position]
    mini = data_treated[0][3][list_position]
    for j in range(2):
        for ik in range(len(data_treated)):
            data = data_treated[ik][3+j][list_position]
            if data < mini:
                mini = data
            elif data > maxi:
                maxi = data
    return mini, maxi


final_data = []

for data_type in range(18):
    if data_type == 0:
        max = 69
        min = 1
        for match in range(len(data_treated)):
            data_treated[match][0] = float_treatment(data_treated[match][0], max, min)
    elif data_type == 1:
        max = 6
        min = 1
        for match in range(len(data_treated)):
            data_treated[match][1] = float_treatment(data_treated[match][1], max, min)
    elif data_type == 2:
        max = 4
        min = 1
        for match in range(len(data_treated)):
            data_treated[match][2] = float_treatment(data_treated[match][2], max, min)
    elif data_type < 9:
        couple = extrema_determination(data_type-3)
        print(couple)
        for match in range(len(data_treated)):
            data_treated[match][3][data_type-3] = float_treatment(data_treated[match][3][data_type-3], couple[0], couple[1])
            data_treated[match][4][data_type - 3] = float_treatment(data_treated[match][4][data_type - 3], couple[0],
                                                                    couple[1])
    elif data_type == 9:
        for match in range(len(data_treated)):
            data_treated[match][3][6] = percentage_treatment(data_treated[match][3][6])
            data_treated[match][4][6] = percentage_treatment(data_treated[match][4][6])
    elif data_type < 13:
        for match in range(len(data_treated)):
            data_treated[match][3][data_type-3] = percentage_treatment([data_treated[match][3][data_type-3]])[0]
            data_treated[match][4][data_type - 3] = percentage_treatment([data_treated[match][4][data_type - 3]])[0]

data_final = []
outcome = []
for i in range(len(data_treated)):
    match = data_treated[i]
    winner = random.randint(0,1)
    if winner == 0:
        outcome += [[1, 0]]
        data_final += [match[0:3] + match[3][:6] + match[3][6] + match[3][7:10] + match[4][:6] + match[4][6] + match[4][7:10]]
    else:
        outcome += [[0, 1]]
        data_final += [
            match[0:3] + match[4][:6] + match[4][6] + match[4][7:10] + match[3][:6] + match[3][6] + match[3][7:10]]

print(data_treated)
print(data_final)

with open('data_to_be_used_final', 'wb') as file:
    my_pickler = pickle.Pickler(file)
    my_pickler.dump([data_final, outcome])
