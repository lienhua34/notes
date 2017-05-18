import tempfile

import tensorflow as tf
# NumPy is often used to load, manipulate and preprocess data.
import numpy as np

from tensorflow.contrib.layers import create_feature_spec_for_parsing
from tensorflow.contrib.learn.python.learn.utils import input_fn_utils

# Declare list of features. We only have one real-valued feature. There are many
# other types of columns that are more complicated and useful.
features = [tf.contrib.layers.real_valued_column("x", dimension=1)]

# An estimator is the front end to invoke training (fitting) and evaluation
# (inference). There are many predefined types like linear regression,
# logistic regression, linear classification, logistic classification, and
# many neural network classifiers and regressors. The following code
# provides an estimator that does linear regression.
estimator = tf.contrib.learn.LinearRegressor(feature_columns=features)

# TensorFlow provides many helper methods to read and set up data sets.
# Here we use `numpy_input_fn`. We have to tell the function how many batches
# of data (num_epochs) we want and how big each batch should be.
x = np.array([1., 2., 3., 4.])
y = np.array([0., -1., -2., -3.])
input_fn = tf.contrib.learn.io.numpy_input_fn({"x":x}, y, batch_size=4,
                                              num_epochs=1000)

# We can invoke 1000 training steps by invoking the `fit` method and passing the
# training data set.
estimator.fit(input_fn=input_fn, steps=1000)

# Here we evaluate how well our model did. In a real example, we would want
# to use a separate validation and testing data set to avoid overfitting.
print(estimator.evaluate(input_fn=input_fn))

# export Estimator
feature_spec = create_feature_spec_for_parsing(features)
serving_input_fn = input_fn_utils.build_parsing_serving_input_fn(feature_spec)

export_model_dir = tempfile.mkdtemp()
export_model_path = estimator.export_savedmodel(
    export_model_dir,
    serving_input_fn)
print("exported model path: {}".format(export_model_path))

# def predict_input_fn():
#     return {'x': tf.constant([1.0, 2.0])}
# print(list(estimator.predict(input_fn=predict_input_fn)))
