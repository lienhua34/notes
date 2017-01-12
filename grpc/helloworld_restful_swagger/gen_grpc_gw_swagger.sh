#!/bin/bash

python -m grpc.tools.protoc -I. \
       -I/usr/local/include \
       -I$GOPATH/src \
       -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
       --swagger_out=logtostderr=true:. \
       pb/helloworld.proto
