import importlib
import tensorflow as tf

def main(_):
    v1 = tf.Variable(tf.constant(123), name="v1")
    v2 = tf.Variable(tf.constant(456), name="v2")
    
    init_op = tf.initialize_all_variables()

    saver = tf.train.Saver({"my_v1": v1})
    
    with tf.Session() as sess:
        sess.run(init_op)
        
        save_path = saver.save(sess, "/tmp/model.ckpt")
        print("v1: %d" % sess.run(v1))
        print("v2: %d" % sess.run(v2))
        print("Model saved in file: %s" % save_path)

if __name__ == "__main__":
    tf.app.run()
