import tensorflow as tf
import numpy as np

board_size = 19

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 1)
    return tf.Variable(intiial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides = [1,1,1,1], padding = 'SAME')

def place_hodlers():
    x = tf.placeholder("float", shape = [None,  board_size, board_size, 8])
    ownership = tf.placeholder("float", shape = [None, board_size**2])
    return x, ownership

def model(x):
    x_board = tf.reshape(x, [-1, board_size, board_size, 8])
    W_conv1 = weight_variable([5, 5, 8, 64])
    b_conv1 = bias_variable([64])
    h_conv1 = tf.nn.relu(conv2d(x_board, W_conv1) + b_conv1)

    W_conv2 = weight_variable([5, 5, 64, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2) + b_conv2)

    W_conv3 = weight_variable([5, 5, 64, 64])
    b_conv3 = bias_variable([64])
    h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3) + b_conv3)
	 
    W_conv4 = weight_variable([5, 5, 64, 48])
    b_conv4 = bias_variable([48])
    h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4) + b_conv4)
	 
    W_conv5 = weight_variable([5, 5, 48, 48])
    b_conv5 = bias_variable([48])
    h_conv5 = tf.nn.relu(conv2d(h_conv4, W_conv5) + b_conv5)
	 
	# Final outputs from layer 5
    W_convm5 = weight_variable([5, 5, 48, 1])
    b_convm5 = bias_variable([1])
    h_convm5 = conv2d(h_conv5, W_convm5) + b_convm5
	
    pred_ownership = tf.sigmoid(tf.reshape(h_convm5, [-1, board_size**2]))
    return pred_ownership

def loss(y_pred, y_true):
    return tf.reduce_mean(tf.pow(y_pred - y_true), 2)

def train(loss):
    return tf.train.AdamOptimizer(1e-3).minimize(loss)

