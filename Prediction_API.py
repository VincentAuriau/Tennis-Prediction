from keras.models import load_model
import pickle
import keras


# MODEL PARAMETERS

model_year = 2012
model = load_model('prediction_model.h5')

with open('indicators_dicts_%i' % model_year, 'rb') as file:
    my_Unpickler = pickle.Unpickler(file)
    [tournaments_dict, level_dict, surface_dict, extrema_dict] = my_Unpickler.load()


# INPUT DATA

# Match
tournament = ''
surface = ''
level = ''

# Player 1

rank_p1 = ''
points_p1 = ''
hand_p1 = ''
height_p1 = ''
fatigue_p1 = ''
age_p1 = ''

percentages_p1 = ''

last_matches_win_percentages_p1 = '' # Last 5 matches
last_matches_surface_p1 = '' # Last 5 matches
win_percentage_actual_over_other_p1 = ''

name_p1 = ''


# Player 2

rank_p2 = ''
points_p2 = ''
hand_p2 = ''
height_p2 = ''
fatigue_p2 = ''
age_p2 = ''

percentages_p2 = ''

last_matches_win_percentages_p2 = '' # Last 5 matches
last_matches_surface_p2 = '' # Last 5 matches
win_percentage_actual_over_other_p2 = ''

name_p2 = ''

# TREATMENT FUNCTIONS

def percentage_treatment(percentage_list):
    return_list = []
    for percentage in percentage_list:
        return_list.append(percentage * 0.01)
    return return_list


def float_treatment(floated, maxi, mini):
    return (2 / (maxi - mini)) * floated - ((maxi + mini) / (maxi - mini))

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

# Last_matches_win_percentage

p2_data.append(percentage_treatment(last_matches_win_percentages_p2))

# Last matches surface win percentage

p2_data.append(percentage_treatment(last_matches_surface_p2))

# Win percentage over P1

p2_data.append(percentage_treatment(win_percentage_actual_over_other_p1))
