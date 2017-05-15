import os
import json

import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators import run_config

cluster = {'ps': ['host1:2222', 'host2:2222'],
           'worker': ['host3:2222', 'host4:2222', 'host5:2222']}

os.environ['TF_CONFIG'] = json.dumps({
    'cluster': cluster,
    'environment': 'CLOUD',
    'task': {
        'type': 'worker',
        'index': 0
    }})

config = run_config.ClusterConfig()
print("master:{}".format(config.master))
print("task_id:{}".format(config.task_id))
print("num_ps_replicas:{}".format(config.num_ps_replicas))
print("task_type:{}".format(config.task_type))
print("is_chief:{}".format(config.is_chief))
