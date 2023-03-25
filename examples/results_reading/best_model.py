import os

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

df_results = pd.read_csv('../../results/20212022/results.csv', sep=";")

best_row = df_results.iloc[df_results.precision.argmax()]
print(best_row)

eval_id = best_row["eval_ID"]
best_results = pd.read_csv(os.path.join("../../results/20212022", f"{eval_id}.csv"), sep=";")

fig, ax = plt.subplots()
df_ww = best_results.loc[best_results.Winner==0].loc[best_results.y_pred==0]
plt.scatter(df_ww.diff_rank, df_ww.Winner, c="tab:pink", label="Well Predicted")
df_wl = best_results.loc[best_results.Winner==0].loc[best_results.y_pred==1]
plt.scatter(df_wl.diff_rank, df_wl.Winner+0.1, c="tab:blue", label="Predicted Wrong")
df_ll = best_results.loc[best_results.Winner==1].loc[best_results.y_pred==1]
plt.scatter(df_ll.diff_rank, df_ll.Winner, c="tab:orange", label="Well Wrong")
df_lw = best_results.loc[best_results.Winner==1].loc[best_results.y_pred==0]
plt.scatter(df_lw.diff_rank, df_lw.Winner-0.1, c="tab:red", label="Predicted Wrong")
plt.legend()

plt.xlabel('Rank Player 0 - Rank Player 1')
plt.ylabel('Winner')
plt.show()
