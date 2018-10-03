from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
from keras import optimizers
import pickle
import pandas as pd
import numpy
import matplotlib.pyplot as plt

with open('data_to_be_used_final', 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    data = my_unpickler.load()

outcomes_df = pd.DataFrame(data[1])
data_df = pd.DataFrame(data[0])

simple_data = []
for i in range(len(data[0])):
    simple_data += [[data[0][i][4],data[0][i][23]]]
train_x_prime = pd.DataFrame(simple_data, columns=['w', 'l'])

#print(train_x_prime[:10])

columns = []
for i in range(41):
    columns += ['x_%i' % (i+1)]
print(columns)

train_x = pd.DataFrame(data[0], columns=columns)
train_y = pd.DataFrame(data[1], columns=['y_1', 'y_2'])

train_x_prime.to_csv('train_x_prime.csv', index=False, header=False)
train_y.to_csv('train_y.csv', index=False)

total = pd.concat([train_x_prime, train_y], axis=1)
total_2 = pd.concat([train_x, train_y], axis=1)
print(total)
print('DELETE MISSING VALUES')
print(total.iloc[58])
print(total.iloc[59])
total = total.dropna()
print(total.iloc[58])
print(total.iloc[59])

total_2 = total_2.sample(frac=1).reset_index(drop=True)

train_x_prime = total.ix[:, ['w', 'l']]

total_2 = total_2.dropna()

train_x = total_2.ix[:, columns]
train_y = total_2.ix[:, ['y_1', 'y_2']]

print('RESTORATION')
print(train_x)
print(train_y)

X_prime = train_x_prime.values[:2200]
X = train_x.values[:2200]
Y = train_y.values[:2200]

X_test = train_x.values[2201:]
Y_test = train_y.values[2201:]

print('CALCUL DES LONGUEURS')
print(Y, len(X))


model = Sequential()
model.add(Dense(100, input_dim=41, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=10, verbose=1)

#scores = model.evaluate(X_test, Y_test)
#print(model.metrics_names)

# X_test = numpy.array([[0.2, -0.5]])
# print(X[:10])
# Z1 = model.predict(X[2220:2320])
# Z2 = Y_test[20:120]
#
# print(Z1)
# print(Z2)
# print(pd.concat([train_x['x_4'][2221:2231], train_x['x_23'][2221:2231]], axis=1))
#

def return_original_float(val, maxmin):
    return 0.5*(val*(maxmin[1] - maxmin[0]) + (maxmin[1] + maxmin[0]))

with open('reversed_indicators_dicts', 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    [reverse_tournament_dict, reverse_surface_dict, extrema_dict] = my_unpickler.load()

print('DISPLAYING THE DATA & THE PREDICTION :')
print('Surface :')
print(train_x['x_1'][2225])
print(train_x['x_3'][2225])
print(reverse_surface_dict[train_x['x_3'][2225]])
print(reverse_tournament_dict[train_x['x_1'][2225]])

print('Ranks & Points')
print(train_x['x_4'][2225], train_x['x_5'][2225])
print(train_x['x_23'][2225], train_x['x_24'][2225])
print(train_x.iloc[2225]['x_4'])
print(train_x['x_4'][2225])
# print(extrema_dict[3], extrema_dict[4])

print(return_original_float(train_x['x_4'][2225], extrema_dict[3]), return_original_float(train_x['x_5'][2225], extrema_dict[4]))
print(return_original_float(train_x['x_23'][2225], extrema_dict[3]), return_original_float(train_x['x_24'][2225], extrema_dict[4]))

print(model.predict(train_x.values[2225:2226]))
print(train_y.values[2225:2226])
# print(model.predict(train_x.values[2225]))


print(train_x['x_4'][2])
print(train_x.iloc[2]['x_4'])
print(train_x)
