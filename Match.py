import ast

import numpy as np

class Match:

    def __init__(self, winner, loser, tournament, surface):
        self.winner = winner
        self.loser = loser
        self.tournament = tournament
        self.surface = surface
        self.tournament_date = ''
        self.tournament_level = ''
        self.round = ''
        self.data = None

    def __str__(self):
        return 'TOURNAMENT : ' + self.tournament + ' W : ' + self.winner + ' L : ' + self.loser

    def get_data(self):
        return [[self.tournament, self.tournament_level, self.surface, self.tournament_date,
                 self.round], self.winner.get_data(), self.loser.get_data()]

    def instantiate(self, tournament_date, tournament_level, tournament_round):
        self.tournament_date = tournament_date
        self.tournament_level = tournament_level
        self.round = tournament_round

        self.data = self.get_data()

    def randomize_positions(self):

        decision = np.random.rand()
        if decision > 0.5:
            return np.concatenate([self.data[0], self.data[1], self.data[2], [0]]).tolist()
        else:
            return np.concatenate([self.data[0], self.data[2], self.data[1], [1]]).tolist()

    def player_data_formatting(self, position):
        data_dict = {}
        # Straight Forward data
        data_dict['name'] = self.data[position][0]
        data_dict['id'] = self.data[position][1]
        data_dict['ranking'] = self.data[position][2]
        data_dict['ranking_points'] = self.data[position][3]

        # Age
        born_year = ast.literal_eval(self.data[position][4][:4])
        match_year = ast.literal_eval(self.tournament_date[:4])
        data_dict['age'] = match_year - born_year

        # Specific Versus
        specific_versus = self.data[position][5].get([self.winner, self.loser][position].id)
        specific_win_percentage = specific_versus.count('V') / len(specific_versus)
        specific_last_matches = specific_versus[-5:].count('V') / 5
        data_dict['specific_versus'] = specific_win_percentage
        data_dict['last_specific_versus'] = specific_last_matches
        ### ADD: LAST FIVE MATCHES + LAST SPECIFIC FIVE MATCHES

        # Straight Forward data #2
        data_dict['hand'] = self.data[position][6]
        #### TO RECHECK ARGUMENT POSITIONING !!! 
        data_dict['height'] = self.data[position][7]
        data_dict['global_win_percentage'] = self.data[position][8]
        data_dict['surface_win_percentage'] = self.data[position][{'clay': 9, 'carpet': 10, 'grass': 11,
                                                                   'carpet': 12}.get(self.surface)]


