from keras.models import load_model
import pickle
import keras
import pandas as pd


def retrieve_percentages(player_id, srface):
    df_players = pd.read_csv('Players_Statistics/Players_Statistics_.csv')
    df = df_players.loc[df_players['id'] == player_id]
    df = df.reset_index(drop=True)
    victory_percentage = df['victory_percentage'][0]
    victory_percentage_surface = df['%s_victory_percentage' % srface.lower()][0]
    ace_percentage = df['ace_percentage'][0]
    doublefaults_percentage = df['doublefault_percentage'][0]
    first_serve_success = df['first_serve_success_percentage'][0]
    winning_on_first_serve = df['winning_on_1st_serve_percentage'][0]
    winning_on_second_serve = df['winning_on_2nd_serve_percentage'][0]
    overall_win_on_serve = df['overall_win_on_serve_percentage'][0]
    break_points_faced = df['breakpoint_faced_percentage'][0]
    break_points_saved = df['breakpoint_saved_percentage'][0]
    return[victory_percentage, victory_percentage_surface, ace_percentage, doublefaults_percentage, first_serve_success,
           winning_on_first_serve, winning_on_second_serve, overall_win_on_serve, break_points_faced, break_points_saved]

# MODEL PARAMETERS

model_year = 2012
model = load_model('prediction_model.h5')

with open('indicators_dicts_%i' % model_year, 'rb') as file:
    my_Unpickler = pickle.Unpickler(file)
    [tournaments_dict, level_dict, surface_dict, extrema_dict] = my_Unpickler.load()


# INPUT DATA

# Match
tournament = 'Wimbledon'
surface = 'Grass'
level = 'G'

# Player 1

name_p1 = 'Roberto Bautista Agut'
id_p1 = 105138

rank_p1 = 19
points_p1 = 1645
hand_p1 = 'R'
height_p1 = 181
fatigue_p1 = 3.8
age_p1 = 31

percentages_p1 = retrieve_percentages(id_p1, surface)
print('PERCENTAGES P1:', percentages_p1)

last_matches_win_percentages_p1 = 0.60  # Last 5 matches
last_matches_surface_p1 = 0.60  # Last 5 matches
win_percentage_actual_over_other_p1 = 0.67


# Player 2

name_p2 = 'Taylor Harry Fritz'
id_p2 = 126203

rank_p2 = 40
points_p2 = 1090
hand_p2 = 'R'
height_p2 = 193
fatigue_p2 = 4
age_p2 = 22

percentages_p2 = retrieve_percentages(id_p2, surface)
print('PERCENTAGES P2:', percentages_p2)

last_matches_win_percentages_p2 = 0.80  # Last 5 matches
last_matches_surface_p2 = 0.80  # Last 5 matches
win_percentage_actual_over_other_p2 = 0.33

# TREATMENT FUNCTIONS


def percentage_treatment(prctg):
    if prctg > 1:
        return 0.01 * prctg
    else:
        return prctg


def float_treatment(floated, maximum, minimum):
    return (2 / (maximum - minimum)) * floated - ((maximum + minimum) / (maximum - minimum))


data_treated = []

# TREATMENT TO FEED THE NETWORK

# Match

match_data = []

# Tournament

maxi = 69
mini = 1

if tournament in tournaments_dict.keys():
    match_data.append(float_treatment(tournaments_dict[tournament], maxi, mini))
elif 'Davis' in tournament:
    match_data.append(float_treatment(69, maxi, mini))
else:
    print('--  New Tournament  --')
    print(tournament)
    match_data.append(float_treatment(70, maxi, mini))

# Level

maxi = 6
mini = 1
match_data.append(float_treatment(level_dict[level], maxi, mini))

# Surface

maxi = 4
mini = 1
match_data.append(float_treatment(surface_dict[surface], maxi, mini))

# Player 1

p1_data = []

# Rank

couple = extrema_dict[3]
p1_data.append(float_treatment(rank_p1, couple[1], couple[0]))

# Points

couple = extrema_dict[4]
p1_data.append(float_treatment(points_p1, couple[1], couple[0]))

# Hand

if hand_p1 == 'L':
    p1_data.append(0)
else:
    p1_data.append(1)

# Height

couple = extrema_dict[6]
p1_data.append(float_treatment(height_p1, couple[1], couple[0]))

# Fatigue

couple = extrema_dict[7]
p1_data.append(float_treatment(fatigue_p1, couple[1], couple[0]))

# Age

couple = extrema_dict[8]
p1_data.append(float_treatment(age_p1, couple[1], couple[0]))

# Percentages

for percentage in percentages_p1:
    p1_data.append(percentage_treatment(percentage))

# Last_matches_win_percentage

p1_data.append(percentage_treatment(last_matches_win_percentages_p1))

# Last matches surface win percentage

p1_data.append(percentage_treatment(last_matches_surface_p1))

# Win percentage over P2

p1_data.append(percentage_treatment(win_percentage_actual_over_other_p2))

# Player 2

p2_data = []

# Rank

couple = extrema_dict[3]
p2_data.append(float_treatment(rank_p2, couple[1], couple[0]))

# Points

couple = extrema_dict[4]
p2_data.append(float_treatment(points_p2, couple[1], couple[0]))

# Hand

if hand_p2 == 'L':
    p2_data.append(0)
else:
    p2_data.append(1)

# Height

couple = extrema_dict[6]
p2_data.append(float_treatment(height_p2, couple[1], couple[0]))

# Fatigue

couple = extrema_dict[7]
p2_data.append(float_treatment(fatigue_p2, couple[1], couple[0]))

# Age

couple = extrema_dict[8]
p2_data.append(float_treatment(age_p2, couple[1], couple[0]))

# Percentages

for percentage in percentages_p2:
    p2_data.append(percentage_treatment(percentage))

# Last_matches_win_percentage

p2_data.append(percentage_treatment(last_matches_win_percentages_p2))

# Last matches surface win percentage

p2_data.append(percentage_treatment(last_matches_surface_p2))

# Win percentage over P1

p2_data.append(percentage_treatment(win_percentage_actual_over_other_p2))

input_data = match_data + p1_data + p2_data
print('P2 data:', p2_data)
print(input_data)
input_data = pd.DataFrame([input_data])
print(input_data)
prediction = model.predict(input_data.values)

print('Prediction: ', prediction)

print('What will ne the results?')
print(name_p1, ':', prediction[0][0]*100, '% Chances of victory')
print(name_p2, ':', prediction[0][1]*100, '% Chances of victory')
