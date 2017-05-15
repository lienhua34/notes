import time
import os

from examples.mnist import input_data
import tensorflow as tf
import caicloud_dist_tensorflow_base as caicloud

class CaicloudDistMnist(caicloud.CaicloudDistTensorflowBase):
    def build_model(self):
        self.__step = 0
        
        # Build model ...
        mnist = input_data.read_data_sets("/caicloud/dist-tf/base/examples/mnist/data", one_hot=True)

        self.__mnist = mnist
            
        # Create the model
        x = tf.placeholder(tf.float32, [None, 784], name='x')
        self.__x = x
        W = tf.Variable(tf.zeros([784, 10]), name='weights')
        tf.histogram_summary("weights", W)
        b = tf.Variable(tf.zeros([10]), name='bias')
        tf.histogram_summary("bias", b)
        y = tf.matmul(x, W) + b

        # Define loss and optimizer
        y_ = tf.placeholder(tf.float32, [None, 10], name='y_')
        self.__y_ = y_
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
        self.__loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
        
        global_step = tf.Variable(0, name='global_step')
        self.__global_step = global_step
        
        train_op = tf.train.AdagradOptimizer(0.01).minimize(
            cross_entropy, global_step=global_step)
        self.__train_op = train_op
        
        # Test trained model
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        self.__accuracy = accuracy

        return global_step

    def train(self, session):
        start_time = time.time()
        self.__step += 1
        
        batch_xs, batch_ys = self.__mnist.train.next_batch(100)
        feed_dict = {self.__x: batch_xs, self.__y_: batch_ys}
        
        _, loss_value = session.run(
            [self.__train_op, self.__loss],
            feed_dict=feed_dict)

        duration = time.time() - start_time
        
        if self.__step % 100 == 0:
            print('Step %d: loss = %.2f (%.3f sec)' % (self.__step, loss_value, duration))
                                            
        if self.__step % 1000 == 0:
            self.compute_accuracy(session)
        
        
    def after_train(self, session):
        print("train done.")
        self.compute_accuracy(session)

    def compute_accuracy(self, session):
        print("Accuracy:")
        print("\tTraining Data: %.3f" % session.run(self.__accuracy,
                                                    feed_dict={
                                                        self.__x: self.__mnist.train.images,
                                                        self.__y_: self.__mnist.train.labels}))
        print("\tValidation Data: %.3f" % session.run(self.__accuracy,
                                                      feed_dict={
                                                          self.__x: self.__mnist.validation.images,
                                                          self.__y_: self.__mnist.validation.labels}))
        print("\tTest Data: %.3f" % session.run(self.__accuracy,
                                                feed_dict={
                                                    self.__x: self.__mnist.test.images,
                                                    self.__y_: self.__mnist.test.labels}))
        
