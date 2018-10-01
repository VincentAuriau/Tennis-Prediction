from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
from keras import optimizers
import pickle
import pandas as pd
import numpy

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

train_x_prime = total.ix[:, ['w', 'l']]

total_2 = total_2.dropna()

train_x = total_2.ix[:, columns]
train_y = total_2.ix[:, ['y_1', 'y_2']]

print('RESTORATION')
print(train_x_prime)
print(train_y)

X = train_x.values[:2200]
Y = train_y.values[:2200]

X_test = train_x.values[2201:]
Y_test = train_y.values[2201:]
print(Y[:10])


model = Sequential()
model.add(Dense(100, input_dim=41, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=100, verbose=1)

scores = model.evaluate(X_test, Y_test)
print(model.metrics_names)

# X_test = numpy.array([[0.2, -0.5]])
# print(X[:10])
print(model.predict(X_test[10:20]))
print(Y_test[10:20])
print(pd.concat([train_x['x_4'][2211:2221], train_x['x_23'][2211:2221]], axis=1))

print('SCORE : ', scores)
