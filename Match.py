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

    def random_data_formatting(self):

        decision = np.random.rand()
        if decision > 0.5:
            return [].extend(self.data[0]).extend(self.data[1]).extend(self.data[2]).extend(0)
        else:
            return [].extend(self.data[0]).extend(self.data[2]).extend(self.data[1]).extend(1)
