import pandas as pd

df_all = pd.read_csv('../Data/atp_players.csv', names=['id', 'LastName', 'SurName', 'Hand', 'BirthDate', 'Country'])
print(df_all.head())

df_2019 = pd.read_csv('../Players_Statistics/Players_Statistics_2019.csv')
print(df_2019.head())


print(df_all.columns)
print(df_2019.columns)

for index, row in df_all.iterrows():
    print(row['BirthDate'])
    date = row['BirthDate']
    if date is not 'nan':
        if date > 1980:
            print(row['LastName'])
