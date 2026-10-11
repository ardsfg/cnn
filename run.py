import numpy as np
import board
import os
import tensorflow as tf
import parsedata
import boardclaude as bc
import model

directory = os.fsencode("/Users/ray/cnn/9d")

pd = parsedata.parseData(directory)
pd.parseAll()
# pd.shuffle()

input = []
output = []
for i in pd.data:
    input.append(i[0])
    if(i[1] == 1):
        output.append([1,0])
    else:
        output.append([0,1])

input = tf.convert_to_tensor(np.array(input))
output = tf.convert_to_tensor(np.array(output))

batchSize = 64

training_data = tf.data.Dataset.from_tensor_slices((input, output))
training_data = training_data.batch(batchSize)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation = 'relu', padding = 'same', use_bias = True, input_shape = (19, 19, 4)))
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding = 'same', use_bias=True))
# model.add(tf.keras.layers.Conv2D(48, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Conv2D(48, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Conv2D(1, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Flatten())
# model.add(tf.keras.layers.Dense(64, activation = 'relu'))
model.add(tf.keras.layers.Dense(2, activation = 'softmax'))
model.summary()

model.compile(optimizer = 'adam', loss = tf.keras.losses.MeanSquaredError())

model.fit(training_data, epochs = 10)