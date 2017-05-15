from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools

import pandas as pd
import tensorflow as tf
import tensorflow.contrib.learn as learn

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

def input_fn(data_set):
    feature_cols = {k: tf.constant(data_set[k].values)
                    for k in FEATURES}
    labels = tf.constant(data_set[LABEL].values)
    return feature_cols, labels

run_config = tf.contrib.learn.RunConfig(save_checkpoints_secs=1)
regressor = tf.contrib.learn.DNNRegressor(
    feature_columns=feature_cols,
    hidden_units=[10, 10],
    model_dir="/tmp/boston_model",
    config=run_config)

experiment = learn.Experiment(
    estimator = regressor,
    train_input_fn = lambda: input_fn(training_set),
    eval_input_fn = lambda: input_fn(test_set),
    train_steps = 5000,
    eval_steps = 1)

# Parameter Server
if run_config.task_type and run_config.task_type == learn.TaskType.PS:
    print("Start PS on {} ...".format(run_config.master))
    experiment.run_std_server()

if run_config.is_chief:
    print("This is chief worker on {} ...".format(run_config.master))
    experiment.train(0)

    # Evaluating the Model
    ev = experiment.evaluate(1)
    loss_score = ev["loss"]
    print("Loss: {0:f}".format(loss_score))
    
else:
    print("This is a worker on {}".format(run_config.master))
    # Training the Model
    # regressor.fit(input_fn=lambda: input_fn(training_set), steps=5000)
    experiment.train(0)

# Making Predictions
# y = regressor.predict(input_fn=lambda: input_fn(prediction_set))
# .predict() returns an iterator; convert to a list and print predictions
# predictions = list(itertools.islice(y, 6))
# print ("Predictions: {}".format(str(predictions)))
