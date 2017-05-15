from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools

import tensorflow as tf
import pandas as pd
import numpy as np

tf.logging.set_verbosity(tf.logging.INFO)
    
# Data Sets
IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"

COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
LABEL = "species"


# Load datasets.
training_set = pd.read_csv(
    IRIS_TRAINING,
    skipinitialspace=True,
    skiprows=1,
    names=COLUMNS)
test_set = pd.read_csv(
    IRIS_TEST,
    skipinitialspace=True,
    skiprows=1,
    names=COLUMNS)

# Specify that all features have real-value data
feature_columns = [tf.contrib.layers.real_valued_column(k)
                   for k in FEATURES]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units=[10, 20, 10],
    n_classes=3,
    model_dir="/tmp/iris_model")

def input_fn(data_set):
    feature_cols = {k: tf.constant(data_set[k].values)
                    for k in FEATURES}
    labels = tf.constant(data_set[LABEL].values)
    return feature_cols, labels

# Fit model
classifier.fit(input_fn=lambda: input_fn(training_set), steps=2000)

# Evaluate accuracy
ev = classifier.evaluate(input_fn=lambda: input_fn(test_set), steps=1)
accuracy_score = ev["accuracy"]
print("Accuracy: {0:f}".format(accuracy_score))

# Classify two new flower samples.
# new_samples = np.array(
#     [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
# p = classifier.predict(new_samples, as_iterable=True)
# y = list(itertools.islice(p, 2))
# print('Predictions: {}'.format(str(y)))

