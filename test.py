import numpy as np
import board
import os
import parsedata
import board
import tensorflow as tf
import random


# directory = os.fsencode("/Users/ray/cnn/data_test_folder")

# pd = parsedata.parseData(directory)
# pd.parseAll()
# pd.shuffle()



directory = os.fsencode("/Users/ray/cnn/9d")

# def getList2(file):
#     f = open(file, 'r', errors = 'ignore')
#     s = f.read()
#     a = s.split("RE[")
#     del a[0]
#     s = a[0]
#     if(s[0] == 'W'):
#         result = -1
#     else:
#         result = 1
#     a = s.split("[")
#     moves = []
#     for i in range(4, len(a)):
#         st = a[i][:2]
#         row = ord(st[0]) - 97
#         col = ord(st[1]) - 97
#         moves.append([row, col])
#     return moves

# i = 0

# for file in os.listdir(directory): # 16161 files
#     file = file.decode("utf-8")
#     file = "/Users/ray/cnn/9d/" + file
#     i+=1
#     print(file)
#     print(i)
#     l = getList2(file)
#     b = board.board(19, 1)
#     ctr = 1
#     for move in l:
#         b.move(move)
    


pd = parsedata.parseData(directory)
pd.parseAll()
pd.shuffle()

input = []
output = []
for i in pd.data:
    input.append(i[0])
    output.append(i[1])

input = tf.convert_to_tensor(np.array(input))
output = tf.convert_to_tensor(np.array(output))

batchSize = 64

training_data = tf.data.Dataset.from_tensor_slices((input, output))
training_data = training_data.batch(batchSize)

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

model.fit(training_data, epochs = 10)

