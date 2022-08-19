import numpy as np
import pandas as pd

from player import Player
from match import Match

df_players = pd.read_csv('Data/atp_players.csv', header=None,
                         names=["ID", "Name", "Surname", "Hand", "BirthDate", "Nationality"],
                         encoding="ISO-8859-1")

print(df_players.head())