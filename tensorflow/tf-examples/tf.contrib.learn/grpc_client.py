# coding=utf-8
# Copyright 2017 Caicloud authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import print_function

import tensorflow as tf
from caicloud.clever.serving.client import grpc_client as serving_grpc_client

def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
  
def run():
    client = serving_grpc_client.GRPCClient('localhost:50051')

    print("""
#######################################
Case1: request.output_filter 为空，计算所有所有输出。
    Request: x = 10
    Expect: 10*0.5 + 2 = 7
#######################################""")
    feature_dict = {
        'x': _float_feature(value=1.0)
    }
    example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
    serialized = example.SerializeToString()
    
    inputs1 = {
        'inputs': tf.contrib.util.make_tensor_proto(serialized, shape=[1]),
    }
    outputs1 = client.call_predict(inputs1)
    print(outputs1)
    result1 = tf.contrib.util.make_ndarray(outputs1['outputs'])
    print('Response: y = {}'.format(result1))

if __name__ == '__main__':
    run()
