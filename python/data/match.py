import ast

import pandas as pd
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
        self.match_time_players_data = {
            "winner": {
                "id": self.winner,
                "age": 0,
                "rank": 0,
                "ranking_points": 0,
                "aces_nb": 0,
                "df_nb": 0,

                "w_svpt": 0,
                "w_1stIn": 0,
                "w_1stWon": 0,
                "w_2ndWon": 0,
                "w_SvGms": 0,
                "w_bpSaved": 0,
                "w_bpFaced": 0
            },
            "loser": {
                "id": self.loser,
                "age": 0,
                "rank": 0,
                "ranking_points": 0,
                "aces_nb": 0,
                "df_nb": 0,

                "w_svpt": 0,
                "w_1stIn": 0,
                "w_1stWon": 0,
                "w_2ndWon": 0,
                "w_SvGms": 0,
                "w_bpSaved": 0,
                "w_bpFaced": 0

            }
        }

        self.sets_number = 0
        self.score = None
        self.elapsed_minutes = None
        self.best_of = None

    def get_rankings(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["rank"], self.match_time_players_data["winner"]["ranking_points"]
        else:
            return self.match_time_players_data["loser"]["rank"], self.match_time_players_data["loser"]["ranking_points"]

    def get_aces_nb(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["aces_nb"]
        else:
            return self.match_time_players_data["loser"]["aces_nb"]

    def get_service_points_played(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["w_svpt"]
        else:
            return self.match_time_players_data["loser"]["w_svpt"]

    def get_df_nb(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["df_nb"]
        else:
            return self.match_time_players_data["loser"]["df_nb"]

    def get_first_serve_win(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["w_1stWon"]
        else:
            return self.match_time_players_data["loser"]["w_1stWon"]

    def get_second_serve_win(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["w_2ndWon"]
        else:
            return self.match_time_players_data["loser"]["w_2ndWon"]

    def get_first_services_in(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["w_1stIn"]
        else:
            return self.match_time_players_data["loser"]["w_1stIn"]

    def get_breakpoint_faced(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["w_bpFaced"]
        else:
            return self.match_time_players_data["loser"]["w_bpFaced"]

    def get_breakpoint_saved(self, player_id):
        if player_id == self.winner.id:
            return self.match_time_players_data["winner"]["w_bpSaved"]
        else:
            return self.match_time_players_data["loser"]["w_bpSaved"]

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

    def get_predictable_data_and_update_players_stats(self):
        match_data = pd.DataFrame({
            "tournament": [self.tournament],
            "tournament_level": [self.tournament_level],
            "round": [self.round],
            "best_of": [self.best_of]
        })

        w_data = self.winner.get_data_df()
        l_data = self.loser.get_data_df()

        self.winner.update_from_match(self)
        self.loser.update_from_match(self)
        return match_data, w_data, l_data

    def get_match_data_results_statistics(self):
        match_statistics = {
            "score": [self.score],
            "elapsed_minutes": [self.elapsed_minutes]
        }

        winner_statistics = {
            "aces_nb": [self.match_time_players_data["winner"]["aces_nb"]],
            "doublefaults_nb": [self.match_time_players_data["winner"]["df_nb"]],
            "svpt": [self.match_time_players_data["winner"]["w_svpt"]],
            "1stIn": [self.match_time_players_data["winner"]["w_1stIn"]],
            "1stWon": [self.match_time_players_data["winner"]["w_1stWon"]],
            "2ndWon": [self.match_time_players_data["winner"]["w_2ndWon"]],
            "SvGms": [self.match_time_players_data["winner"]["w_SvGms"]],
            "bpSaved": [self.match_time_players_data["winner"]["w_bpSaved"]],
            "bpFaced": [self.match_time_players_data["winner"]["w_bpFaced"]]
        }
        loser_statistics = {
            "aces_nb": [self.match_time_players_data["loser"]["aces_nb"]],
            "doublefaults_nb": [self.match_time_players_data["loser"]["df_nb"]],
            "svpt": [self.match_time_players_data["loser"]["w_svpt"]],
            "1stIn": [self.match_time_players_data["loser"]["w_1stIn"]],
            "1stWon": [self.match_time_players_data["loser"]["w_1stWon"]],
            "2ndWon": [self.match_time_players_data["loser"]["w_2ndWon"]],
            "SvGms": [self.match_time_players_data["loser"]["w_SvGms"]],
            "bpSaved": [self.match_time_players_data["loser"]["w_bpSaved"]],
            "bpFaced": [self.match_time_players_data["loser"]["w_bpFaced"]]
        }

        return pd.DataFrame(match_statistics), pd.DataFrame(winner_statistics), pd.DataFrame(loser_statistics)

    def instantiate_from_data_row(self, data_row):

        self.tournament_date = data_row["tourney_date"]
        self.tournament_level = data_row["tourney_level"]
        self.round = data_row["round"]
        self.sets_number = len(str(data_row["score"]).split("-"))

        self.score = data_row["score"]
        self.elapsed_minutes = data_row["minutes"]
        self.best_of = data_row["best_of"]

        self.match_time_players_data = {
            "winner": {
                "id": data_row["winner_id"],
                "age": data_row["winner_age"],
                "rank": data_row["winner_rank"],
                "ranking_points": data_row["winner_rank_points"],
                "aces_nb": data_row["w_ace"],
                "df_nb": data_row["w_df"],

                "w_svpt": data_row["w_svpt"],
                "w_1stIn": data_row["w_1stIn"],
                "w_1stWon": data_row["w_1stWon"],
                "w_2ndWon": data_row["w_2ndWon"],
                "w_SvGms": data_row["w_SvGms"],
                "w_bpSaved": data_row["w_bpSaved"],
                "w_bpFaced": data_row["w_bpFaced"]
            },
            "loser": {
                "id": data_row["loser_id"],
                "age": data_row["loser_age"],
                "rank": data_row["loser_rank"],
                "ranking_points": data_row["loser_rank_points"],
                "aces_nb": data_row["l_ace"],
                "df_nb": data_row["l_df"],

                "w_svpt": data_row["l_svpt"],
                "w_1stIn": data_row["l_1stIn"],
                "w_1stWon": data_row["l_1stWon"],
                "w_2ndWon": data_row["l_2ndWon"],
                "w_SvGms": data_row["l_SvGms"],
                "w_bpSaved": data_row["l_bpSaved"],
                "w_bpFaced": data_row["l_bpFaced"]

            }
        }

    def positions_randomized_data(self):

        decision = np.random.rand()
        match_conditions = {}
        match_conditions['tournament'] = self.tournament
        match_conditions['tournament_level'] = self.tournament_level
        match_conditions['tournament_date'] = self.tournament_date
        match_conditions['surface'] = self.surface
        match_conditions['round'] = self.round
        if decision > 0.5:
            return [match_conditions, self.player_data_formatting(1), self.player_data_formatting(2), {'winner': 0}]
            # return np.concatenate([self.data[0], self.data[1], self.data[2], [0]]).tolist()
        else:
            return [match_conditions, self.player_data_formatting(2), self.player_data_formatting(1), {'winner': 1}]
            # return np.concatenate([self.data[0], self.data[2], self.data[1], [1]]).tolist()

    def player_data_formatting(self, position):
        data_dict = {}
        # Straight Forward data
        data_dict['name'] = self.data[position][0]
        data_dict['id'] = self.data[position][1]
        data_dict['ranking'] = self.data[position][2]
        data_dict['ranking_points'] = self.data[position][3]

        # Age
        born_year = int(self.data[position][4]//10000)
        match_year = ast.literal_eval(self.tournament_date[:4])
        data_dict['age'] = match_year - born_year

        # Specific Versus
        specific_versus = self.data[position][5].get([self.loser, self.winner][position-1].id, [])
        if len(specific_versus) == 0:
            specific_win_percentage = -1
        else:
            specific_win_percentage = specific_versus.count('V') / len(specific_versus)

        if len(specific_versus[-5:]) > 0:
            specific_last_matches = specific_versus[-5:].count('V') / len(specific_versus[-5:])
        else:
            specific_last_matches = -1
        data_dict['specific_versus'] = specific_win_percentage
        data_dict['last_specific_versus'] = specific_last_matches

        # Straight Forward data #2
        data_dict['hand'] = self.data[position][6]
        data_dict['height'] = self.data[position][8]

        # Win percentages global/surface
        if len(self.data[position][9][-5:]) > 0:
            last_matches = self.data[position][9][-5:].count('V') / len(self.data[position][9][-5:])
        else:
            last_matches = -1
        data_dict['last_matches'] = last_matches
        if len(self.data[position][{'Clay': 10, 'Carpet': 11, 'Grass': 12,
                                                    'Hard': 13}.get(self.surface)][-5:]) > 0:
            last_matches_surface = self.data[position][{'Clay': 10, 'Carpet': 11, 'Grass': 12,
                                                        'Hard': 13}.get(self.surface)][-5:].count('V') / len(self.data[position][{'Clay': 10, 'Carpet': 11, 'Grass': 12,
                                                        'Hard': 13}.get(self.surface)][-5:])
        else:
            last_matches_surface = -1
        data_dict['last_matches_surface'] = last_matches_surface
        data_dict['global_win_percentage'] = self.data[position][14]
        data_dict['surface_win_percentage'] = self.data[position][{'Clay': 15, 'Carpet': 16, 'Grass': 17,
                                                                   'Hard': 18}.get(self.surface)]

        # Straight Forward data #3
        data_dict['ace_percentage'] = self.data[position][19]
        data_dict['doublefault_percentage'] = self.data[position][20]
        data_dict['first_serve_success_percentage'] = self.data[position][21]
        data_dict['winning_on_1st_serve_percentage'] = self.data[position][22]
        data_dict['winning_on_2nd_serve_percentage'] = self.data[position][23]
        data_dict['overall_win_on_serve_percentage'] = self.data[position][24]
        data_dict['break_point_faced_percentage'] = self.data[position][25]
        data_dict['break_point_saved_percentage'] = self.data[position][26]
        data_dict['fatigue'] = self.data[position][27]

        return data_dict




