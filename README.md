# Tennis-Prediction Repository

The goal of this project is to predict the outcome of a tennis match using the data of both players.
The data used comes from https://github.com/JeffSackmann.

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

### Loading players statistics at match time + match outcome

```python
from data.data_loader import matches_data_loader
data_df = matches_data_loader(path_to_data="submodules/tennis_atp")
```

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
)

print("Test Score", test_score)
```