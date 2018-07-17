class Player:

    def __init__(self, name, born_year, country, nb_id):
        self.name = name
        self.born_year = born_year
        self.ranking = 0
        self.ranking_over_time = 0
        self.country = country
        self.id = nb_id
        self.last_tournament_date = ''
        self.versus = {}
        self.hand = ''
        self.height = 0

        self.last_matches = ['', '', '', '', '']
        self.matches = []
        self.victory_percentage = 0

        self.matches_hard = []
        self.hard_victory_percentage = 0
        self.matches_carpet = []
        self.carpet_victory_percentage = 0
        self.matches_clay = []
        self.clay_victory_percentage = 0
        self.matches_grass = []
        self.grass_victory_percentage = 0

        self.ace_percentage = 0
        self.ace_proportion = []

        self.fatigue = 0
        self.fatigue_features = {'previous tournament': ['19000000', 0, 0], 'current tournament': ['19000000', 0, 0]}

    def __str__(self):
        return 'ID : ' + str(self.id) + ' *** Name : ' + self.name + ' '*(35 - len(self.name)) + ' *** Born Year : ' \
               + str(self.born_year) + ' *** Country : ' + str(self.country) + ' *** Hand : ' + str(self.hand) \
               + ' *** Height : ' + str(self.height)

    def add_victory(self, id_loser):
        self.last_matches[4] = self.last_matches[3]
        self.last_matches[3] = self.last_matches[2]
        self.last_matches[2] = self.last_matches[1]
        self.last_matches[1] = self.last_matches[0]
        self.last_matches[0] = 'V'
        if id_loser in self.versus.keys():
            self.versus[id_loser].append('V')
        else:
            self.versus[id_loser] = ['V']
        self.update_victory_percentage('V')

    def add_defeat(self, id_winner):
        self.last_matches[4] = self.last_matches[3]
        self.last_matches[3] = self.last_matches[2]
        self.last_matches[2] = self.last_matches[1]
        self.last_matches[1] = self.last_matches[0]
        self.last_matches[0] = 'D'
        if id_winner in self.versus.keys():
            self.versus[id_winner].append('D')
        else:
            self.versus[id_winner] = ['D']
        self.update_victory_percentage('D')

    def update_victory_percentage(self, match_outcome):
        self.matches.append(match_outcome)
        victories_number = self.matches.count('V')
        matches_number = len(self.matches)
        self.victory_percentage = (victories_number / matches_number) * 100

    def update_surface_victory_percentage(self, surface, outcome):
        if surface == 'Clay':
            self.matches_clay.append(outcome)
            self.clay_victory_percentage = self.matches_clay.count('V') / len(self.matches_clay) * 100
            print(self.clay_victory_percentage)
            print(self.matches_clay)
        elif surface == 'Grass':
            self.matches_grass.append(outcome)
            self.grass_victory_percentage = self.matches_grass.count('V') / len(self.matches_grass) * 100
            print(self.grass_victory_percentage)
        elif surface == 'Hard':
            self.matches_hard.append(outcome)
            self.hard_victory_percentage = self.matches_hard.count('V') / len(self.matches_hard) * 100
            print(self.hard_victory_percentage)
        elif surface == 'Carpet':
            self.matches_carpet.append(outcome)
            self.carpet_victory_percentage = self.matches_carpet.count('V') / len(self.matches_carpet) * 100
            print(self.carpet_victory_percentage)

    def update_fatigue(self, tournament_date, sets_number):
        if tournament_date == self.fatigue_features['current tournament'][0]:
            self.fatigue_features['current tournament'][1] += sets_number
            self.fatigue_features['current tournament'][2] += 1
        else:
            self.fatigue_features['previous tournament'][0] = self.fatigue_features['current tournament'][0]
            self.fatigue_features['current tournament'][0] = tournament_date
            self.fatigue_features['previous tournament'][1] = self.fatigue_features['current tournament'][1]
            self.fatigue_features['current tournament'][1] = sets_number
            self.fatigue_features['current tournament'][2] = 1

        previous_tournament_date = self.fatigue_features['previous tournament'][0]
        current_tournament_date = self.fatigue_features['current tournament'][0]

        days_difference_tournaments = (int(current_tournament_date[:4]) - int(previous_tournament_date[:4]))*365 \
            + (int(current_tournament_date[4:6]) - int(previous_tournament_date[4:6]))*30 \
            + int(current_tournament_date[6:8]) - int(previous_tournament_date[6:8])

        self.fatigue = self.fatigue_features['previous tournament'][1] / days_difference_tournaments \
            + self.fatigue_features['current tournament'][1]
        print('fatigue', self.fatigue)

    def update_ace_percentage(self, aces_nb, service_points_played):
        self.ace_proportion += [[aces_nb, service_points_played]]
        total_aces_nbr = 0
        total_service_points_played = 0
        for proportion in self.ace_proportion:
            total_aces_nbr += proportion[0]
            total_service_points_played += proportion[1]
        self.ace_percentage = total_aces_nbr / total_service_points_played * 100
