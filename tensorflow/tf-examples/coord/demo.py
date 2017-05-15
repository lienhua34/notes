import threading
import tensorflow as tf

def MyLoop(coord, id):
    count = 0
    while not coord.should_stop():
        print("in thread %d, count: %d" % (id, count))
        if count == 100:
            coord.request_stop()
        count += 1

coord = tf.train.Coordinator()
threads = [threading.Thread(target=MyLoop, args=(coord, i)) for i in xrange(10)]

for t in threads:
    t.start()
coord.join(threads)
