from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators import estimator
import numpy as np

# Data Sets
IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"

def main(unused_argv):
    # Load datasets.
    training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=IRIS_TRAINING,
        target_dtype=np.int,
        features_dtype=np.float32)
    test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=IRIS_TEST,
        target_dtype=np.int,
        features_dtype=np.float32)

    # Specify that all features have real-value data
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]
    
    # Build 3 layer DNN with 10, 20, 10 units respectively.
    dnnClassifier = tf.contrib.learn.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[10, 20, 10],
        n_classes=3,
        model_dir="/tmp/iris_model",
        config=tf.contrib.learn.RunConfig(save_checkpoints_secs=1))
    classifier = estimator.SKCompat(dnnClassifier)

    # var_names = dnnClassifier.get_variable_names()
    # print("Variable names:{}".format(var_names))

    # Fit model
    classifier.fit(x=training_set.data,
                   y=training_set.target,
                   max_steps=2000)
    
    # Evaluate accuracy
    scores = classifier.score(x=test_set.data, y=test_set.target)
    print("Accuracy: {0:f}".format(scores["accuracy"]))
    print("global_step: {0}".format(scores["global_step"]))
    print("auc: {0}".format(scores["auc"]))
    print("loss: {0}".format(scores["loss"]))

    # Classify two new flower samples.
    new_samples = np.array(
        [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
    y_predicted = classifier.predict(new_samples)
    print('Predictions: {}'.format(str(y_predicted)))

if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
