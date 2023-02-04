import ast

import pandas as pd
import numpy as np


class Match:
    def __init__(self, winner, loser, tournament, surface):
        self.winner = winner
        self.loser = loser
        self.tournament = tournament
        self.surface = surface

        self.tournament_date = ""
        self.tournament_level = ""
        self.round = ""
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
                "w_bpFaced": 0,
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
                "w_bpFaced": 0,
            },
        }

        self.sets_number = 0
        self.score = None
        self.elapsed_minutes = None
        self.best_of = None

    def get_rankings(self, player_id):
        if player_id == self.winner.id:
            return (
                self.match_time_players_data["winner"]["rank"],
                self.match_time_players_data["winner"]["ranking_points"],
            )
        else:
            return (
                self.match_time_players_data["loser"]["rank"],
                self.match_time_players_data["loser"]["ranking_points"],
            )

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
        return (
            "TOURNAMENT : "
            + self.tournament
            + " W : "
            + self.winner
            + " L : "
            + self.loser
        )

    def get_prior_data_and_update_players_stats(self):
        match_data = pd.DataFrame(
            {
                "tournament": [self.tournament],
                "tournament_level": [self.tournament_level],
                "round": [self.round],
                "best_of": [self.best_of],
            }
        )

        w_data = self.winner.get_data_df()
        lr, lrp = self.winner.get_last_months_rankings(
            date=self.tournament_date, nb_months=12, day_of_month="last"
        )
        w_data["last_rankings"] = [lr]
        w_data["last_ranking_points"] = [lrp]
        l_data = self.loser.get_data_df()
        lr, lrp = self.loser.get_last_months_rankings(
            date=self.tournament_date, nb_months=12, day_of_month="last"
        )
        l_data["last_rankings"] = [lr]
        l_data["last_ranking_points"] = [lrp]

        self.winner.update_from_match(self)
        self.loser.update_from_match(self)
        return match_data, w_data, l_data

    def get_match_data_results_statistics(self):
        match_statistics = {
            "score": [self.score],
            "elapsed_minutes": [self.elapsed_minutes],
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
            "bpFaced": [self.match_time_players_data["winner"]["w_bpFaced"]],
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
            "bpFaced": [self.match_time_players_data["loser"]["w_bpFaced"]],
        }

        return (
            pd.DataFrame(match_statistics),
            pd.DataFrame(winner_statistics),
            pd.DataFrame(loser_statistics),
        )

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
                "w_bpFaced": data_row["w_bpFaced"],
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
                "w_bpFaced": data_row["l_bpFaced"],
            },
        }
