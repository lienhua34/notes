import tensorflow as tf

def main(_):
    v = tf.constant("hello World")

    sv = tf.train.Supervisor(logdir='/tmp/mydir')
    sess = sv.prepare_or_wait_for_session("")
    while not sv.should_stop():
        print(sess.run(v))
        sv.request_stop()

if __name__ == "__main__":
    tf.app.run()
