import pickle
import random

model_year = 2012
year_to_treat = 2013

with open('Data_%i' % year_to_treat, 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    data_not_treated = my_unpickler.load()

with open('indicators_dicts_%i' % model_year, 'rb') as file:
    my_Unpickler = pickle.Unpickler(file)
    [tournaments_dict, level_dict, surface_dict, extrema_dict] = my_Unpickler.load()

print(data_not_treated[0])

data_treated = []

for match_not_treated in data_not_treated:
    match_data_treated = []

    # Match
    tournament = match_not_treated[0][0]

    if tournament in tournaments_dict.keys():
        match_data_treated.append(tournaments_dict[tournament])
    elif 'Davis' in tournament:
        match_data_treated.append(69)
    else:
        print('--  New Tournament  --')
        print(tournament)
        match_data_treated.append(70)

    level = match_not_treated[0][1]
    match_data_treated.append(level_dict[level])

    surface = match_not_treated[0][2]
    match_data_treated.append(surface_dict[surface])

    # print(match_data_treated)

    for player in range(1, 3):

        # Players

        # Name

        name = match_not_treated[player][0]

        # Ranking
        ranking = match_not_treated[player][2]
        # print(ranking)

        # Ranking points
        points = match_not_treated[player][3]
        # print(points)

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
        # print(fatigue)

        # Age
        year = year_to_treat
        if match_not_treated[player][4] != 'nan' and match_not_treated[player][4] == match_not_treated[player][4]:
            age = year - int(match_not_treated[player][4])
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
        # print(results_actual_against_other)
        win_percentage_actual_over_other = results_actual_against_other.count('V') / \
                                           len(results_actual_against_other) * 100

        # print(win_percentage_actual_over_other)

        player_data_treated = [ranking, points, hand, height, fatigue, age, percentages, last_matches_win_percentage,
                               last_matches_surface, win_percentage_actual_over_other, name]

        match_data_treated += [player_data_treated]

    # print(match_data_treated)
    data_treated += [match_data_treated]
print('DATA treated', data_treated[0])


def percentage_treatment(percentage_list):
    return_list = []
    for percentage in percentage_list:
        return_list.append(percentage * 0.01)
    return return_list


def float_treatment(floated, maxi, mini):
    return (2 / (maxi - mini)) * floated - ((maxi + mini) / (maxi - mini))

for data_type in range(19):
    if data_type == 0:
        maxi = 69
        mini = 1
        for match in range(len(data_treated)):
            data_treated[match][0] = float_treatment(data_treated[match][0], maxi, mini)

    elif data_type == 1:
        maxi = 6
        mini = 1
        for match in range(len(data_treated)):
            data_treated[match][1] = float_treatment(data_treated[match][1], maxi, mini)

    elif data_type == 2:
        maxi = 4
        mini = 1
        for match in range(len(data_treated)):
            data_treated[match][2] = float_treatment(data_treated[match][2], maxi, mini)
        for key in surface_dict.keys():
            surface_dict[key] = float_treatment(surface_dict[key], maxi, mini)

    elif data_type < 9:
        couple = extrema_dict[data_type]
        for match in range(len(data_treated)):
            data_treated[match][3][data_type - 3] = float_treatment(data_treated[match][3][data_type-3], couple[1],
                                                                    couple[0])
            data_treated[match][4][data_type - 3] = float_treatment(data_treated[match][4][data_type - 3], couple[1],
                                                                    couple[0])

    elif data_type == 9:
        for match in range(len(data_treated)):
            data_treated[match][3][6] = percentage_treatment(data_treated[match][3][6])
            data_treated[match][4][6] = percentage_treatment(data_treated[match][4][6])

    elif data_type < 13:
        for match in range(len(data_treated)):
            data_treated[match][3][data_type - 3] = percentage_treatment([data_treated[match][3][data_type - 3]])[0]
            data_treated[match][4][data_type - 3] = percentage_treatment([data_treated[match][4][data_type - 3]])[0]

print(data_treated[0])
# print(data_treated)

data_final = []
outcome = []
for i in range(len(data_treated)):
    match = data_treated[i]
    winner = random.randint(0,1)
    if winner == 0:
        outcome += [[1, 0]]
        data_final += [match[0:3] + match[3][:6] + match[3][6] + match[3][7:10] + match[4][:6] + match[4][6] + match[4][7:10] + [match[3][10]] + [match[4][10]]]
    else:
        outcome += [[0, 1]]
        data_final += [
            match[0:3] + match[4][:6] + match[4][6] + match[4][7:10] + match[3][:6] + match[3][6] + match[3][7:10] + [match[4][10]] + [match[3][10]]]

print(data_final[0])

with open('data_to_be_used_final_%i' % year_to_treat, 'wb') as file:
    my_pickler = pickle.Pickler(file)
    my_pickler.dump([data_final, outcome])
