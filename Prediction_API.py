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
ranking_points_p1 = ''
hand_p1 = ''
height_p1 = ''
fatigue_p1 = ''
age_p1 = ''

percentages_p1 = ''

last_matches_win_percentages_p1 = ''
last_matches_surface_p1 = ''
win_percentage_actual_over_other_p1 = ''

name_p1 = ''


# Player 2

rank_p2 = ''
ranking_points_p2 = ''
hand_p2 = ''
height_p2 = ''
fatigue_p2 = ''
age_p2 = ''

percentages_p2 = ''

last_matches_win_percentages_p2 = ''
last_matches_surface_p2 = ''
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
if tournament in tournaments_dict.keys():
    match_data.append(tournaments_dict[tournament])
elif 'Davis' in tournament:
    match_data.append(69)
else:
    print('--  New Tournament  --')
    print(tournament)
    match_data.append(70)

# Level

match_data.append(level_dict[level])

# Surface

match_data.append(surface_dict[surface])

# Player 1

if hand_p1 == 'L':
    hand = 0
else:
    hand = 1