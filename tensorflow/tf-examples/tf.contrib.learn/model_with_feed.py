import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

_c = None

# Declare list of features, we only have one real-valued feature
def model(features, labels, mode):
  global _c
  
  # Build a linear model and predict values
  W = tf.get_variable("W", [1], dtype=tf.float64)
  b = tf.get_variable("b", [1], dtype=tf.float64)
  _c = tf.placeholder(dtype=tf.float64, name="c", shape=[1])
  # _c = tf.constant(1, dtype=tf.float64, name="c")
  y = W*features['x'] + b + _c
  # Loss sub-graph
  loss = tf.reduce_sum(tf.square(y - labels))
  # Training sub-graph
  global_step = tf.train.get_global_step()
  optimizer = tf.train.GradientDescentOptimizer(0.01)
  train = tf.group(optimizer.minimize(loss),
                   tf.assign_add(global_step, 1))
  # ModelFnOps connects subgraphs we built to the
  # appropriate functionality.
  return tf.contrib.learn.ModelFnOps(
      mode=mode, predictions=y,
      loss= loss,
      train_op=train)



estimator = tf.contrib.learn.Estimator(model_fn=model)

_input_tensor = None
_output_tensor = None
def input_fn():
  global _input_tensor, _output_tensor
  _input_tensor = tf.placeholder(dtype=tf.float64, shape=[None], name='x')
  _output_tensor = tf.placeholder(dtype=tf.float64, shape=[None], name='y')
  return {'x': _input_tensor}, _output_tensor
# input_fn = tf.contrib.learn.io.numpy_input_fn({"x": x}, y, 4, num_epochs=1000)

# define our data set
x=np.array([1., 2., 3., 4.])
y=np.array([0., -1., -2., -3.])

hooks = [
  tf.train.FeedFnHook(
    lambda: {_c: [3], _input_tensor: x, _output_tensor: y})
]

# train
estimator.fit(input_fn=input_fn, steps=1000, monitors=hooks)
# evaluate our model
print(estimator.evaluate(input_fn=input_fn, steps=10, hooks=hooks))
