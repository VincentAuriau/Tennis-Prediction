import numpy as np
import pandas as pd
import ast


df_all = pd.read_csv('../Data/atp_players.csv', names=['id', 'LastName', 'SurName', 'Hand', 'BirthDate', 'Country'])
print(df_all.head())

df_2019 = pd.read_csv('../Players_Statistics/Players_Statistics_2019.csv')
print(df_2019.head())


print(df_all.columns)
print(df_2019.columns)

IDs_to_keep = []
Names = []
for index, row in df_all.iterrows():
    date = row['BirthDate']
    if date is not 'nan':
        if date > 19800000:
            # print(row['LastName'], row['SurName'])
            id = row['id']
            row_19 = df_2019.loc[df_2019.id == id]
            if len(row_19) > 0:
                if len(ast.literal_eval(row_19['versus'].iloc[0]).keys()) > 10:
                    print(row['id'])
                    print(row_19['name'])
                    print(row_19['versus'])
                    IDs_to_keep.append(row['id'])
                    Names.append(row_19['name'].iloc[0])

print(Names)
np.save('IDs_2019.npy', np.array(IDs_to_keep))

