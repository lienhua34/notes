from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import tempfile

import pandas as pd
import tensorflow as tf

from tensorflow.contrib.layers import create_feature_spec_for_parsing
from tensorflow.contrib.learn.python.learn.utils import input_fn_utils

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

regressor = tf.contrib.learn.DNNRegressor(
    feature_columns=feature_cols,
    hidden_units=[10, 10],
    model_dir="/tmp/boston_model",
    config=tf.contrib.learn.RunConfig(save_checkpoints_secs=1))

def input_fn(data_set):
    feature_cols = {k: tf.constant(data_set[k].values)
                    for k in FEATURES}
    labels = tf.constant(data_set[LABEL].values)
    return feature_cols, labels

# Training the Model
regressor.fit(input_fn=lambda: input_fn(training_set), steps=5000)

# Evaluating the Model
ev = regressor.evaluate(input_fn=lambda: input_fn(test_set), steps=1)
loss_score = ev["loss"]
print("Loss: {0:f}".format(loss_score))

# Making Predictions
y = regressor.predict(input_fn=lambda: input_fn(prediction_set))
# .predict() returns an iterator; convert to a list and print predictions
predictions = list(itertools.islice(y, 6))
print ("Predictions: {}".format(str(predictions)))

# export model
feature_spec = create_feature_spec_for_parsing(feature_cols)
serving_input_fn = input_fn_utils.build_parsing_serving_input_fn(feature_spec)

export_model_dir = tempfile.mkdtemp()
export_model_path = regressor.export_savedmodel(
    export_model_dir,
    serving_input_fn)
print("exported model path: {}".format(export_model_path))


