#!/bin/bash

docker run -ti \
       -v $(pwd)/hello.py:/hello.py \
       tensorflow/tensorflow:1.0.0 \
       /bin/bash
# python /hello.py
