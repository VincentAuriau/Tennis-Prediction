import pandas as pd
import json

basic_stats = pd.read_csv('Data/atp_players.csv', names = ['id', 'Surname', 'LastName', 'Hand', 'BirthDate', 'Country'])
advanced_stats = pd.read_csv('Players_Statistics/Players_Statistics_2019.csv')

print(basic_stats.head())
print(advanced_stats.head())

# data_id = {'a': {}, 'z': {}, 'e': {}, 'r': {}, 't': {}, 'y': {}, 'u': {}, 'i': {}, 'o': {}, 'p': {},
#            'q': {}, 's': {}, 'd': {}, 'f': {}, 'g': {}, 'h': {}, 'j': {}, 'k': {}, 'l': {}, 'm': {},
#            'w': {}, 'x': {}, 'c': {}, 'v': {}, 'b': {}, 'n': {}}
data_full = {}
data_id = {}

for index, row in basic_stats.iterrows():
    # print(row['id'])
    # print(str(row['BirthDate'])[-4:], str(row['BirthDate'])[-4:] > '70')

    if str(row['BirthDate'])[:4] > '1970' and str(row['BirthDate'])[:4] != 'nan':
        print('selected: ', str(row['BirthDate']))
        # data_id[str(row['Surname'])[0].lower()][str(row['Surname']) + ' ' + str(row['LastName'])] = row['id']
        data_id[str(row['Surname']) + ' ' + str(row['LastName'])] = row['id']
        data_full[row['id']] = {
            'Surname': row['Surname'],
            'LastName': row['LastName'],
            'Hand': row['Hand'],
            'BirthDate': row['BirthDate'],
            'Country': row['Country']
        }

with open('data.json', 'w') as outfile:
    json.dump(data_full, outfile)

with open('data_id.json', 'w') as outfile:
    json.dump(data_id, outfile)
