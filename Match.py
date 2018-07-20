class Match:

    def __init__(self, winner, loser, tournament, surface):
        self.winner = winner
        self.loser = loser
        self.tournament = tournament
        self.surface = surface
        self.tournament_date = ''
        self.tournament_level = ''
        self.round = ''

    def __str__(self):
        return 'TOURNAMENT : ' + self.tournament + ' W : ' + self.winner + ' L : ' + self.loser

    def get_data(self):
        return [[self.tournament, self.tournament_level, self.surface, self.tournament_date, self.tournament_level,
                 self.round], [self.winner.get_data()], [self.loser.get_data()]]
