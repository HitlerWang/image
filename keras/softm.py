import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense

x_train = np.random.random((1000,20))

y_train = np.random.random((1000,20))

x_test = np.random.random((1000,20))

y_test = np.random.random((1000,20))


model = Sequential()
model.add(Dense(units=64 , activation='rele' , input_dim=100) )
model.add(Dense(units=10 , activation='softmax'))

model.compile(loss='categorical_crossentropy' , optimizer='sgd' , metrics=['accuracy'])

model.fit(x_train , y_train , epochs=5 ,batch_size=32)

loss_and_metrics = model.evaluate(x_test , y_test , batch_size=128)

classes = model.predict(x_test , batch_size=128)

