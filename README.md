# Tennis-Prediction Repository

The goal of this project is to predict the outcome of a tennis match using the data of both players.
The data used comes from [Jeff Sackmann's repository](https://github.com/JeffSackmann).

## Installation

To clone the repository, with the data you need to also clone the submodules:

```bash
git clone --recurse-submodules https://github.com/VincentAuriau/Tennis-Prediction.git
```

## Usage

You can find examples in /examples:

### Loading players statistics at match time + match outcome

```python
from data.data_loader import matches_data_loader
data_df = matches_data_loader(path_to_data="submodules/tennis_atp")
```
data_df contains let you access information about players (statistics prior to the match) along statistics of the match.
A basic example statistic: the victory percentage of the best ranked player in a match, depending on players rankings.


Number of ATP main matches depending on players rank             |  Victory % of best ranked player
:-------------------------:|:-------------------------:
![](examples/data/nb_matches.png) |  ![](examples/data/Best_player_win_percentage.png)

It can be easily used to also compute players statistics over their carreer, and/or at match time. Here is a simple example with Stan Wawrinka:
Stan's Victory % in main ATP matches             |  Stan's career aces % diff with adversary
:-------------------------:|:-------------------------:
![](examples/data/stan_the_man_win_percentage.png) |  ![](examples/data/stanimal_aces_percentage_difference.png)

Here is an example of a data row:

| id | tournament    | tournament_level    | tournament_date    | tournament_surface    | round    | best_of    | match_id    | Winner | Score |
| :---:   | :---: | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: |
| atp_matches_qual_chall_2003_5427 | San Benedetto CH   | C   | 20030811   | Clay   | SF   | 3   | 20030811   | 0 | 2-6 7-5 7-5 |

Additional match statistics: elapsed_minutes, aces_nb_1, doublefaults_nb_1, svpt_1, 1stIn_1, 1stWon_1, 2ndWon_1, SvGms_1, bpSaved_1, bpFaced_1, aces_nb_2, doublefaults_nb_2, svpt_2, 1stIn_2, 1stWon_2, 2ndWon_2, SvGms_2 bpSaved_2, bpFaced_2



| Name_1 | ID_1    | Ranking_1    | Ranking_Points_1    | Ranking_History_1    | Best_Rank_1    | Birth_Year_1    | Versus_1    | Hand_1 | Last_Tournament_Date_1    | Height_1    | Matches_1    | Matchs_Clay_1    | Matches_Carpet_1    | Matches_Grass_1    | Matches_Hard_1    | Victories_Percentage_1    | Clay_Victories_Percentage_1    | Carpet_Victories_Percentage_1    | Grass_Victories_Percentage_1    | Hard_Victories_Percentage_1    | Aces_Percentage_1    | Doublefaults_Percentage_1    | First_Save_Success_Percentage_1    | Winning_on_1st_Serve_Percentage_1    | Winning_on_2nd_Serve_Percentage_1    | Overall_Win_on_Serve_Percentage_1    | BreakPoint_Face_Percentage_1 | BreakPoint_Saved_Percentage_1 | last_rankings_1 | last_ranking_points_1 |
| :---:   | :---: | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: |
| Stan.Wawrinka | 104527  | 184   | 114   | {20030616: [387, 68], 20030707: [363, 74], 20030714: [348, 79], 20030721: [303, 99], 20030811: [284, 114]}   | 284   | 19850328   | []   | R | 20030721 | 183 | [['V', 'atp_matches_qual_chall_2003_3466'], ['D', 'atp_matches_qual_chall_2003_3481'], ['D', 'atp_matches_2003_4049'], ['V', 'atp_matches_2003_4315'], ['D', 'atp_matches_2003_4328'], ['V', 'atp_matches_2003_4773'], ['D', 'atp_matches_2003_4782'], ['V', 'atp_matches_qual_chall_2003_5408'], ['V', 'atp_matches_qual_chall_2003_5419'], ['V', 'atp_matches_qual_chall_2003_5424']] | ['V', 'D', 'D', 'V', 'D', 'V', 'D', 'V', 'V', 'V'] | [] | [] | [] | 60 | 60 | 0 | 0 | 0 | 3.41880341880342 | 4.27350427350427 | 64.957264957265 | 54.985754985755 | 15.6695156695157 | 70.6552706552707 | 11.3960113960114 | 7.69230769230769 | [303, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 387] | [99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68] |


| Name_2 | ID_2 | Ranking_2 | Ranking_Points_2 | Ranking_History_2 | Best_Rank_2 | Birth_Year_2 | Versus_2 | Hand_2 | Last_Tournament_Date_2 | Height_2 | Matches_2 | Matchs_Clay_2 | Matches_Carpet_2 | Matches_Grass_2 | Matches_Hard_2 | Victories_Percentage_2 | Clay_Victories_Percentage_2 | Carpet_Victories_Percentage_2 | Grass_Victories_Percentage_2 | Hard_Victories_Percentage_2 | Aces_Percentage_2 | Doublefaults_Percentage_2 | First_Save_Success_Percentage_2 | Winning_on_1st_Serve_Percentage_2 | Winning_on_2nd_Serve_Percentage_2 | Overall_Win_on_Serve_Percentage_2 | BreakPoint_Face_Percentage_2 | BreakPoint_Saved_Percentage_2 | last_rankings_2 | last_ranking_points_2 |
| :---:   | :---: | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: | :---: | :---:   | :---: | :---:   | :---: |
| Martin.Vassallo Arguello | 103506 | 125 | 296 | {19990201: [817, 13], 20000710: [398, 61], 20000731: [354, 75], 20000807: [377, 70], 20010625: [459, 48], 20010709: [405, 61], 20010813: [391, 68], 20010820: [374, 72], 20010827: [342, 88], 20010917: [291, 117], 20010924: [286, 122], 20011008: [238, 154], 20011015: [237, 157], 20011022: [211, 178], 20011112: [206, 181], 20011126: [198, 186], 20011203: [201, 186], 20011231: [202, 186], 20020318: [175, 220], 20020325: [175, 220], 20020401: [178, 213], 20020408: [173, 219], 20020422: [174, 219], etc...} | 123 | 19800210 | []   | R | 20030804 | 183 | [['V', 'atp_matches_qual_chall_1999_380'], ['D', 'atp_matches_qual_chall_1999_393'], ['V', 'atp_matches_qual_chall_2000_3972'], ['V', 'atp_matches_qual_chall_2000_3988'], ['D', 'atp_matches_qual_chall_2000_3996'], ['D', 'atp_matches_qual_chall_2000_4725'], ['D', 'atp_matches_qual_chall_2000_4758'], ['V', 'atp_matches_qual_chall_2001_3699'], ['V', 'atp_matches_qual_chall_2001_3712'], ['D', 'atp_matches_qual_chall_2001_3719'], ['V', 'atp_matches_qual_chall_2001_4080'], ['V', 'atp_matches_qual_chall_2001_4089'], ['D', 'atp_matches_qual_chall_2001_4093'], ['V', 'atp_matches_qual_chall_2001_5286'], ['D', 'atp_matches_qual_chall_2001_5295'], ['V', 'atp_matches_qual_chall_2001_5433'], etc...] | ['V', 'D', 'V', 'V', 'D', 'V', 'V', 'D', 'V', 'V', 'D', 'V', 'D', 'V', 'V', 'D', 'V', 'V', 'V', 'D', 'V', 'D', 'V', 'V', 'V', 'V', 'D', 'D', 'V', 'V', 'V', 'D', 'V', 'D', 'V', 'D', 'D', etc...] | 61.0294117647059 | 63.5593220338983 | 40 | 0 | 50 | 4.82456140350877 | 5.26315789473684 | 61.4035087719298 | 46.4912280701754 | 18.859649122807 | 65.3508771929825 | 9.64912280701754 | 5.70175438596491 | [157, 136, 165, 158, 9999, 9999, 204, 198, 197, 188, 204, 233] | [247, 304, 220, 232, 0, 0, 164, 172, 177, 188, 167, 137] |

### Train/Testing on matches outcome:

```python
from sklearn.ensemble import RandomForestClassifier
from evaluation.train_test import train_test_evaluation

test_score = train_test_evaluation(
    train_years=[2020, 2021],
    test_years=[2022, 2023],
    model_class=RandomForestClassifier,
    model_params={"n_estimators": 2000, "max_depth": None},
    match_features=[],
    player_features=["Ranking"],
    encoding_params={},
    additional_features=[],
    save_path="./results",
    save_all_results=False
)

print("Test Score", test_score)
```

Models and hyperparamters can easily be compared with the file results.csv saved in save_path.

Different models performances
:-------------------------:
![](examples/results_reading/models_performances.png)

If the argument save_all_results is set to True, the whole csv of test data is saved. It helps to get more in-depth analysis of results

Model precision compared with best ranked player wins strategy            |  Model precision depending of players ranks
:-------------------------:|:-------------------------:
![](examples/results_reading/win_per_surface.png) |  ![](examples/results_reading/precision_percentage_players_ranks.png)

### Encoding match
In order to represent history of a player, one can use MatchEncoders:

```python
from history_modeling.encoding_model import PCAMatchEncoder

model = PCAMatchEncoder(num_pca_features=2)
model.fit(data_df, transform_data=True)
X_r, match_info = model.predict(data_df, transform_data=True)
```

2D representation of match outcome:
:-------------------------:
![](examples/history_modeling/2d_pca_match_representation_test.png)
