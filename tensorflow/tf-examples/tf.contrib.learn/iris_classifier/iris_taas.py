from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators import estimator
import numpy as np
from caicloud.clever.tensorflow import dist_base

# Data Sets
IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"

class DistIris(dist_base.CaicloudDistTensorflowBase):
    def build_model(self, global_step, is_chief, sync, num_replicas):
        # Load datasets.
        self.training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=IRIS_TRAINING,
            target_dtype=np.int,
            features_dtype=np.float32)
        self.test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
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
            model_dir="/tmp/iris_model")
        self.classifier = estimator.SKCompat(dnnClassifier)

        return None

    def train(self, session, global_step, is_chief):
        # Fit model
        self.classifier.fit(x=self.training_set.data,
                            y=self.training_set.target,
                            steps=2)
        return False

    def after_train(self, session, is_chief):
        # Evaluate accuracy
        accuracy_score = self.classifier.score(x=self.test_set.data,
                                               y=self.test_set.target)["accuracy"]
        print("Accuracy: {0:f}".format(accuracy_score))

if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    from caicloud.clever.tensorflow import entry as caicloud_entry
    caicloud_entry.start(DistIris)
