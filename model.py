import parsedata
import board
import os
import random
import numpy as np
import tensorflow as tf

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation = 'relu', padding = 'same', use_bias = True, input_shape = (19, 19, 2)))
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Conv2D(48, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Conv2D(48, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Conv2D(1, (5, 5), activation='relu', padding = 'same', use_bias=True))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation = 'relu'))
model.add(tf.keras.layers.Dense(1, activation = 'sigmoid'))
model.summary()

model.compile(optimizer = 'adam', loss = tf.keras.losses.MeanSquaredError())