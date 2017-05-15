#!/bin/bash

docker run -d -P --name=tf-dev-env -v /Users/lienhua34/Programs/python/tf-examples:/tf-examples cargo.caicloud.io/caicloud/tensorflow:0.11.0
echo "started tensorflow demo develop environment..."
