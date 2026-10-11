import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np

board_size = 28

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data(path='mnist.npz')
print(x_train.shape)

train_data = tf.data.Dataset.from_tensor_slices(
    (x_train.reshape([-1, 28, 28, 1]).astype(np.float32) / 255, y_train.astype(np.int32)))
train_data = train_data.shuffle(buffer_size=60000).batch(128).repeat()

test_data = tf.data.Dataset.from_tensor_slices(
    (x_test.reshape([-1, 28, 28, 1]).astype(np.float32) / 255, y_test.astype(np.int32))).batch(128)

train_steps = 2000

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters = 32, kernel_size=(3, 3), padding = "same", activation=tf.nn.relu, name = "conv_1", input_shape = (28, 28, 1)),
    tf.keras.layers.Conv2D(filters = 64, kernel_size=(3, 3), padding = "same", activation=tf.nn.relu, name = "conv_2"),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), name="maxpool_1"),
    tf.keras.layers.Conv2D(filters = 128, kernel_size=(3, 3), padding = "same", activation=tf.nn.relu, name = "conv_3"),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), name="maxpool_2"),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation=tf.nn.relu),
    tf.keras.layers.Dense(5, tf.nn.sigmoid),
    tf.keras.layers.Dense(10)
])

# Adam makes things much smoother
optimizer = tf.optimizers.Adam()
# from_logits = True!! #neverforget
loss_fn = tf.losses.SparseCategoricalCrossentropy(from_logits=True)

model.summary()

train_acc_metric = tf.keras.metrics.SparseCategoricalAccuracy()

for step, (image_batch, label_batch) in enumerate(train_data):
    if step > train_steps:
        break

    with tf.GradientTape() as tape:
        logits = model(image_batch)
        # loss format is generally: first argument targets, second argument outputs
        loss = loss_fn(label_batch, logits)

    # if you didn't build the model, it is important that you get the variables
    # AFTER the model has been called the first time
    variables = model.trainable_variables
    gradients = tape.gradient(loss, variables)

    optimizer.apply_gradients(zip(gradients, variables))

    train_acc_metric(label_batch, logits)

    if not step % 100:
        # this is different from before. there, we only evaluated accuracy
        # for one batch. Now, we always average over 100 batches
        print("Loss: {} Accuracy: {}".format(loss, train_acc_metric.result()))
        train_acc_metric.reset_state()


test_acc_metric = tf.keras.metrics.SparseCategoricalAccuracy()
for image_batch, label_batch in test_data:
    test_acc_metric(label_batch, model(image_batch))
print("Test acc: {}".format(test_acc_metric.result()))
