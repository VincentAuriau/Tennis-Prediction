import numpy as np
import pandas as pd

# How to update player's ranking ?


class Player:
    def __init__(self, name, birthdate, country, nb_id, hand="", height=0):
        self.name = name
        self.birthdate = birthdate

        self.rankings_history = {}
        self.ranking = 9999
        self.ranking_points = 0
        self.ranking_over_time = 0
        self.country = country
        self.id = nb_id
        self.last_tournament_date = ""
        self.versus = {}
        self.hand = hand
        self.height = height

        self.last_matches = ["", "", "", "", ""]
        self.matches = []
        self.victories_percentage = 0

        self.matches_hard = []
        self.hard_victories_percentage = 0
        self.matches_carpet = []
        self.carpet_victories_percentage = 0
        self.matches_clay = []
        self.clay_victories_percentage = 0
        self.matches_grass = []
        self.grass_victories_percentage = 0

        self.aces_percentage = 0

        self.doublefaults_percentage = 0
        self.first_serve_success_percentage = 0
        self.winning_on_1st_serve_percentage = 0
        self.winning_on_2nd_serve_percentage = 0
        self.overall_win_on_serve_percentage = 0

        self.service_data = {
            "service_games_played": [],
            "1st_serve_success": [],
            "aces_nb": [],
            "doublefaults_nb": [],
            "win_on_1st_serve": [],
            "win_on_2nd_serve": [],
            "breakpoints_faced": [],
            "breakpoints_saved": [],
        }

        self.breakpoint_faced_percentage = 0
        self.breakpoint_saved_percentage = 0

        self.fatigue = 0
        self.fatigue_features = {
            "previous tournament": {"date": "19000000", "num_sets": 0, "num_matchs": 0},
            "current tournament": {"date": "19000000", "num_sets": 0, "num_matchs": 0},
        }

    def __str__(self):
        return (
            "ID : "
            + str(self.id)
            + " *** Name : "
            + self.name
            + " " * (35 - len(self.name))
            + " *** Born Year : "
            + str(self.birthdate)
            + " *** Country : "
            + str(self.country)
            + " *** Hand : "
            + str(self.hand)
            + " *** Height : "
            + str(self.height)
        )

    def _add_victory(self, id_loser, tournament_date="19000101"):
        """
        Update last_matches argument with a victories and updates versus argument using id_loser
        :param id_loser: ID of los of match against current player
        :return:
        """
        self.last_matches[4] = self.last_matches[3]
        self.last_matches[3] = self.last_matches[2]
        self.last_matches[2] = self.last_matches[1]
        self.last_matches[1] = self.last_matches[0]
        self.last_matches[0] = "V"
        if id_loser in self.versus.keys():
            self.versus[id_loser].append(["V", tournament_date])
        else:
            self.versus[id_loser] = [["V", tournament_date]]
        self._update_victories_percentage("V")

    def _add_defeat(self, id_winner, tournament_date="19000101"):
        """
        Add a Defeat
        :param id_winner:
        :return:
        """
        self.last_matches[4] = self.last_matches[3]
        self.last_matches[3] = self.last_matches[2]
        self.last_matches[2] = self.last_matches[1]
        self.last_matches[1] = self.last_matches[0]
        self.last_matches[0] = "D"
        if id_winner in self.versus.keys():
            self.versus[id_winner].append(["D", tournament_date])
        else:
            self.versus[id_winner] = [["D", tournament_date]]
        self._update_victories_percentage("D")

    def _update_victories_percentage(self, match_outcome):
        """
        Updates Victories Percentage with a V/D of last match
        :param match_outcome:
        :return:
        """
        self.matches.append(match_outcome)
        victories_number = self.matches.count("V")
        matches_number = len(self.matches)
        self.victories_percentage = (victories_number / matches_number) * 100

    def _update_surfaces_victories_percentage(self, surface, outcome):
        """
        Updates % of victories on a given surface (V/D)
        :param surface:
        :param outcome:
        :return:
        """
        if surface == "Clay":
            self.matches_clay.append(outcome)
            self.clay_victories_percentage = (
                self.matches_clay.count("V") / len(self.matches_clay) * 100
            )

        elif surface == "Grass":
            self.matches_grass.append(outcome)
            self.grass_victories_percentage = (
                self.matches_grass.count("V") / len(self.matches_grass) * 100
            )

        elif surface == "Hard":
            self.matches_hard.append(outcome)
            self.hard_victories_percentage = (
                self.matches_hard.count("V") / len(self.matches_hard) * 100
            )

        elif surface == "Carpet":
            self.matches_carpet.append(outcome)
            self.carpet_victories_percentage = (
                self.matches_carpet.count("V") / len(self.matches_carpet) * 100
            )

    def _update_fatigue(self, tournament_date, sets_number):
        """
        Updates Fatigue arguments: self.fatigue but also self.fatigue_features
        :param tournament_date:
        :param sets_number:
        :return:
        """
        if sets_number == sets_number and sets_number != "nan":
            if tournament_date == self.fatigue_features["current tournament"]["date"]:
                self.fatigue_features["current tournament"]["num_sets"] += sets_number
                self.fatigue_features["current tournament"]["num_matchs"] += 1
            else:
                self.fatigue_features["previous tournament"] = self.fatigue_features[
                    "current tournament"
                ]
                self.fatigue_features["current tournament"] = {
                    "date": tournament_date,
                    "num_sets": sets_number,
                    "num_matchs": 1,
                }

            previous_tournament_date = str(
                self.fatigue_features["previous tournament"]["date"]
            )
            current_tournament_date = str(
                self.fatigue_features["current tournament"]["date"]
            )

            days_difference_tournaments = (
                (int(current_tournament_date[:4]) - int(previous_tournament_date[:4]))
                * 365
                + (
                    int(current_tournament_date[4:6])
                    - int(previous_tournament_date[4:6])
                )
                * 30
                + int(current_tournament_date[6:8])
                - int(previous_tournament_date[6:8])
            )
            self.fatigue = (
                self.fatigue_features["previous tournament"]["num_sets"]
                / days_difference_tournaments
                + self.fatigue_features["current tournament"]["num_sets"]
            )
        else:
            print("NaN in sets number", sets_number)

    def _update_aces_percentage(self, aces_nb):
        """
        Upates Aces Percentage
        :param aces_nb:
        :return:
        """

        if aces_nb == aces_nb and aces_nb != "nan":
            self.service_data["aces_nb"].append(aces_nb)
            total_aces_nbr = sum(self.service_data["aces_nb"])
            total_service_points_played = sum(self.service_data["service_games_played"])

            if total_service_points_played != 0:
                self.aces_percentage = (
                    total_aces_nbr / total_service_points_played * 100
                )
            else:
                print("No point played :", aces_nb)

    def _update_doublefaults_percentage(self, df_nb):
        """
        Update doublefaults percentage
        :param df_nb:
        :return:
        """
        if df_nb == df_nb and df_nb != "nan":
            self.service_data["doublefaults_nb"].append(df_nb)
            total_df_nbr = sum(self.service_data["doublefaults_nb"])
            total_service_points_played = sum(self.service_data["service_games_played"])

            if total_service_points_played != 0:
                self.doublefaults_percentage = (
                    total_df_nbr / total_service_points_played * 100
                )
            else:
                print("No point played :", total_df_nbr)
                self.doublefaults_percentage = 0

        else:
            print("NaN in Double Faults", df_nb)

    def _update_winning_on_1st_serve_percentage(self, first_serve_win):
        """

        :param first_serve_win:
        :return:
        """
        self.service_data["win_on_1st_serve"].append(first_serve_win)

        total_first_serves_win = sum(self.service_data["1st_serve_success"])
        total_service_points_played = sum(self.service_data["service_games_played"])

        if total_service_points_played != 0:
            self.winning_on_1st_serve_percentage = (
                total_first_serves_win / total_service_points_played * 100
            )
        else:
            print("No point played :", total_first_serves_win)

    def _update_winning_on_2nd_serve_percentage(self, second_serve_win):
        """

        :param second_serve_win:
        :return:
        """
        self.service_data["win_on_2nd_serve"].append(second_serve_win)

        total_second_serves_win = sum(self.service_data["win_on_2nd_serve"])
        total_service_points_played = sum(self.service_data["service_games_played"])

        if total_service_points_played != 0:
            self.winning_on_2nd_serve_percentage = (
                total_second_serves_win / total_service_points_played * 100
            )
        else:
            print("No point played :", total_second_serves_win)

    def _update_first_serve_success_percentage(self, first_services_in):
        """

        :param first_services_in:
        :return:
        """
        self.service_data["1st_serve_success"].append(first_services_in)

        total_first_serves_in = sum(self.service_data["1st_serve_success"])
        total_service_points_played = sum(self.service_data["service_games_played"])

        if total_service_points_played != 0:
            self.first_serve_success_percentage = (
                total_first_serves_in / total_service_points_played * 100
            )
        else:
            print("No point played :", total_first_serves_in)

    def _update_breakpoints_faced_and_saved(self, breakpoint_faced, breakpoint_saved):
        """

        :param breakpoint_faced:
        :param breakpoint_saved:
        :return:
        """
        self.service_data["breakpoints_saved"].append(breakpoint_saved)
        self.service_data["breakpoints_faced"].append(breakpoint_faced)

        total_breakpoint_faced = sum(self.service_data["breakpoints_faced"])
        total_games_played = sum(self.service_data["service_games_played"])
        total_breakpoint_saved = sum(self.service_data["breakpoints_saved"])

        if total_games_played != 0:
            self.breakpoint_faced_percentage = (
                total_breakpoint_faced / total_games_played * 100
            )
            self.breakpoint_saved_percentage = (
                total_breakpoint_saved / total_games_played * 100
            )
        else:
            print("No point played :", self.service_data["breakpoints_saved"])

    def _update_service_data(
        self,
        service_games_played,
        aces_nb,
        doublefaults_nb,
        first_serve_success,
        winning_on_1st_serve,
        winning_on_2nd_serve,
        breakpoints_faced,
        breakpoints_saved,
    ):
        # Assert data exists
        if (
            service_games_played == service_games_played
            and aces_nb == aces_nb
            and doublefaults_nb == doublefaults_nb
            and first_serve_success == first_serve_success
            and winning_on_1st_serve == winning_on_1st_serve
            and winning_on_2nd_serve == winning_on_2nd_serve
            and breakpoints_faced == breakpoints_faced
            and breakpoints_saved == breakpoints_saved
        ):
            self.service_data["service_games_played"].append(service_games_played)

            self._update_aces_percentage(aces_nb=aces_nb)
            self._update_doublefaults_percentage(df_nb=doublefaults_nb)
            self._update_winning_on_1st_serve_percentage(
                first_serve_win=winning_on_1st_serve
            )
            self._update_winning_on_2nd_serve_percentage(
                second_serve_win=winning_on_2nd_serve
            )
            self.overall_win_on_serve_percentage = (
                self.winning_on_1st_serve_percentage
                + self.winning_on_2nd_serve_percentage
            )
            self._update_first_serve_success_percentage(
                first_services_in=first_serve_success
            )
            self._update_breakpoints_faced_and_saved(
                breakpoint_saved=breakpoints_saved, breakpoint_faced=breakpoints_faced
            )

        else:
            # Future argument ;)
            verbose = 1
            if verbose > 2:
                print("Service data not complete...")

    def _update_rankings(self, new_ranking, new_ranking_points):
        self.ranking = new_ranking
        self.ranking_points = new_ranking_points

    def _get_best_ranking(self):
        all_ranks = [
            self.rankings_history[date][0] for date in self.rankings_history.keys()
        ]
        return np.min(all_ranks)

    def update_from_match(self, match):
        """
        Updates the whole player profile from a match
        :param match:
        :return:
        """

        # Update Rankings ?

        if match.winner.id == self.id:
            self._add_victory(match.loser.id, tournament_date=match.tournament_date)
            self._update_surfaces_victories_percentage(match.surface, "V")
        else:
            assert match.loser.id == self.id
            self._add_defeat(match.winner.id, tournament_date=match.tournament_date)
            self._update_surfaces_victories_percentage(match.surface, "D")
        self._update_fatigue(match.tournament_date, match.sets_number)

        self._update_service_data(
            service_games_played=match.get_service_points_played(self.id),
            aces_nb=match.get_aces_nb(self.id),
            doublefaults_nb=match.get_df_nb(self.id),
            first_serve_success=match.get_first_services_in(self.id),
            winning_on_1st_serve=match.get_first_serve_win(self.id),
            winning_on_2nd_serve=match.get_second_serve_win(self.id),
            breakpoints_faced=match.get_breakpoint_faced(self.id),
            breakpoints_saved=match.get_breakpoint_saved(self.id),
        )

        self._update_rankings(*match.get_rankings(self.id))
        if self.ranking == self.ranking and isinstance(self.ranking, int):
            self.rankings_history[match.tournament_date] = [
                self.ranking,
                self.ranking_points,
            ]
        else:
            self.rankings_history[match.tournament_date] = [
                9999,
                0,
            ]

    def get_data_df(self, opponent=None):
        data_dict = {
            "Name": [self.name],
            "ID": [self.id],
            "Ranking": [self.ranking],
            "Ranking_Points": [self.ranking_points],
            "Ranking_History": [self.rankings_history],
            "Best_Rank": [self._get_best_ranking()],
            "Birth_Year": [self.birthdate],
            "Versus": [self.versus if opponent is None else self.versus.get(opponent, [])],
            "Hand": [self.hand],
            "Last_Tournament_Date": [
                self.fatigue_features["previous tournament"]["date"]
            ],
            "Height": [self.height],
            "Matches": [self.matches],
            "Matches_Clay": [self.matches_clay],
            "Matches_Carpet": [self.matches_carpet],
            "Matches_Grass": [self.matches_grass],
            "Matches_Hard": [self.matches_hard],
            "Victories_Percentage": [self.victories_percentage],
            "Clay_Victories_Percentage": [self.clay_victories_percentage],
            "Carpet_Victories_Percentage": [self.carpet_victories_percentage],
            "Grass_Victories_Percentage": [self.grass_victories_percentage],
            "Hard_Victories_Percentage": [self.hard_victories_percentage],
            "Aces_Percentage": [self.aces_percentage],
            "Doublefaults_Percentage": [self.doublefaults_percentage],
            "First_Serve_Success_Percentage": [self.first_serve_success_percentage],
            "Winning_on_1st_Serve_Percentage": [self.winning_on_1st_serve_percentage],
            "Winning_on_2nd_Serve_Percentage": [self.winning_on_2nd_serve_percentage],
            "Overall_Win_on_Serve_Percentage": [self.overall_win_on_serve_percentage],
            "BreakPoint_Face_Percentage": [self.breakpoint_faced_percentage],
            "BreakPoint_Saved_Percentage": [self.breakpoint_saved_percentage],
            "Fatigue": [self.fatigue],
        }
        return pd.DataFrame(data_dict)

    def get_last_months_rankings(self, date, nb_months=12, day_of_month="last"):
        assert day_of_month in [
            "last",
            "first",
        ], f"For now you can only use first or last month day for ranking, you chose {day_of_month}"
        if day_of_month == "last":
            f = max
        else:
            f = min
        date = str(date)
        last_months_ranks = [9999 for _ in range(nb_months)]
        last_months_points = [0 for _ in range(nb_months)]
        date_year = int(date[:4])
        date_month = int(date[4:6])

        for i in range(nb_months):
            if date_month == 1:
                date_month = 12
                date_year = date_year - 1
            else:
                date_month = date_month - 1

            days_with_rankings = []
            for key in self.rankings_history.keys():
                if f"{date_year}{date_month:02d}" in str(key):
                    days_with_rankings.append(int(str(key)[6:]))
            try:
                if len(days_with_rankings) > 0:
                    last_months_ranks[-i] = self.rankings_history[
                        int(f"{date_year}{date_month:02d}{f(days_with_rankings):02d}")
                    ][0]
                    last_months_points[-i] = self.rankings_history[
                        int(f"{date_year}{date_month:02d}{f(days_with_rankings):02d}")
                    ][1]

            except:
                print(days_with_rankings)
                print(self.rankings_history)
                print(date_month, date_year)

                print(f"{date_year}{date_month:02d}{f(days_with_rankings):02d}")
                print(
                    self.rankings_history[
                        f"{date_year}{date_month:02d}{f(days_with_rankings):02d}"
                    ]
                )
                raise ValueError

        return last_months_ranks, last_months_points
