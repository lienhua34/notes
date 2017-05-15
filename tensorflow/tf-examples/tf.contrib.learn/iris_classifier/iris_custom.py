import tensorflow.contrib.learn as learn
from sklearn import datasets, metrics
import tensorflow as tf
import tensorflow.contrib.layers as layers
import tensorflow.contrib.learn as learn

iris = datasets.load_iris()

def my_model(features, labels):
    """DNN with three hidden layers."""
    # Convert the labels to a one-hot tensor of shape (length of features, 3) and
    # with a on-value of 1 for each one-hot vector of length 3.
    labels = tf.one_hot(labels, 3, 1, 0)

    # Create three fully connected layers respectively of size 10, 20, and 10.
    features = layers.stack(features, layers.fully_connected, [10, 20, 10])

    # Create two tensors respectively for prediction and loss.
    predictions, loss = (
        tf.contrib.learn.models.logistic_regression(features, labels)
    )

    # Create a tensor for training op.
    train_op = tf.contrib.layers.optimize_loss(
        loss,
        tf.contrib.framework.get_global_step(),
        optimizer='Adagrad',
        learning_rate=0.1)

    return {
        'class': tf.argmax(predictions, 1),
        'prob': predictions
        }, loss, train_op

classifier = learn.Estimator(model_fn=my_model)
classifier.fit(iris.data, iris.target, steps=1000, batch_size=32)

y_predictions = [
    p['class'] for p in classifier.predict(iris.data, as_iterable=True)]
score = metrics.accuracy_score(iris.target, y_predictions)
print("Accuracy: {0:f}".format(score))
