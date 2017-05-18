from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools

import pandas as pd
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

COLUMNS = ["crim", "zn", "indus", "nox", "rm", "age",
           "dis", "tax", "ptratio", "medv"]
FEATURES = ["crim", "zn", "indus", "nox", "rm",
            "age", "dis", "tax", "ptratio"]
LABEL = "medv"

training_set = pd.read_csv("boston_train.csv", skipinitialspace=True,
                           skiprows=1, names=COLUMNS)
test_set = pd.read_csv("boston_test.csv", skipinitialspace=True,
                       skiprows=1, names=COLUMNS)
prediction_set = pd.read_csv("boston_predict.csv", skipinitialspace=True,
                             skiprows=1, names=COLUMNS)

feature_cols = [tf.contrib.layers.real_valued_column(k)
                for k in FEATURES]

_input_tensors = None
_output_tensor = None
regressor = tf.contrib.learn.DNNRegressor(
    feature_columns=feature_cols,
    hidden_units=[10, 10],
    model_dir="/tmp/boston_model",
    config=tf.contrib.learn.RunConfig(save_checkpoints_secs=1))

def input_fn():
    global _input_tensors, _output_tensor
    _input_tensors = {k: tf.placeholder(dtype=tf.float64, shape=[None], name=k)
                      for k in FEATURES}
    _output_tensor = tf.placeholder(dtype=tf.float64, shape=[None], name=LABEL)
    return _input_tensors, _output_tensor

def feed_fn(data_set):
    global _input_tensors, _output_tensor
    feed_dict = {_input_tensors[k]: data_set[k].values
                 for k in FEATURES}
    feed_dict[_output_tensor] = data_set[LABEL].values
    return feed_dict

train_monitors = [tf.train.FeedFnHook(lambda: feed_fn(training_set))]
eval_hooks = [tf.train.FeedFnHook(lambda: feed_fn(test_set))]

# Training the Model
regressor.fit(input_fn=input_fn, steps=5000, monitors=train_monitors)

# Evaluating the Model
ev = regressor.evaluate(input_fn=input_fn, steps=1, hooks=eval_hooks)
loss_score = ev["loss"]
print("Loss: {0:f}".format(loss_score))
