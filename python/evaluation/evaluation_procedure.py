import pandas as pd

df = pd.read_csv("test_data_df.csv")

print(df.head())


# Define the transformations of data to numerical
def cat_col_to_onehot_encode(df, column):
    values = df[column].unique()
    values_dict = {}
    int_value = 0
    for val in values:
        values_dict[val] = int_value
        int_value += 1
    for i in range(len(df)):
        df[column].iloc[i] = values_dict[df[column].iloc[i]]
    return df


df = df.fillna(0)
df = cat_col_to_onehot_encode(df, "hand_1")
df = cat_col_to_onehot_encode(df, "hand_0")
df = cat_col_to_onehot_encode(df, "round")
df = cat_col_to_onehot_encode(df, "surface")
df = cat_col_to_onehot_encode(df, "tournament")
df = cat_col_to_onehot_encode(df, "tournament_level")

x_cols = list(df.columns)
print(x_cols)
x_cols.remove("winner")
x_cols.remove("Unnamed: 0")
x_cols.remove("id_0")
x_cols.remove("id_1")
x_cols.remove("name_0")
x_cols.remove("name_1")
x_cols.remove("tournament_date")
print(x_cols)
X = df[x_cols].values
Y = df["winner"].values


print(X.shape, Y.shape)
print(X[0])
print("___")
print(Y[:10])


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold


kf = KFold(n_splits=5, shuffle=True)
scores = []
for train_index, test_index in kf.split(X):
    clf = RandomForestClassifier(max_depth=None, random_state=0, n_estimators=10000)
    clf.fit(X[train_index], Y[train_index])
    score = clf.score(X[test_index], Y[test_index])
    scores.append(score)

print("score: ", sum(scores) / len(scores))
print(scores)


from sklearn import svm


kf = KFold(n_splits=5, shuffle=True)
scores = []
for train_index, test_index in kf.split(X):
    clf = svm.SVC()
    clf.fit(X[train_index], Y[train_index])
    score = clf.score(X[test_index], Y[test_index])
    scores.append(score)
