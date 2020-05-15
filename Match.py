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

    def player_data_formatting(self):
        pass