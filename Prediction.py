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

train_x = pd.DataFrame(data[0][:10])
train_y = pd.DataFrame(data[1], columns=['w', 'l'])['w']

train_x_prime.to_csv('train_x_prime.csv', index=False, header=False)
train_y.to_csv('train_y.csv', index=False)

X = train_x_prime.values
Y = train_y.values
print(Y)

model = Sequential()
model.add(Dense(12, input_dim=2, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, epochs=150, batch_size=10)
# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
