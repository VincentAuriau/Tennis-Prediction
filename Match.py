class Match:

    def __int__(self, winner, loser, tournament, surface):
        self.winner = winner
        self.loser = loser
        self.tournament = tournament
        self.surface = surface

    def __str__(self):
        return 'TOURNAMENT : ' + self.tournament + ' W : ' + self.winner + ' L : ' + self.loser
