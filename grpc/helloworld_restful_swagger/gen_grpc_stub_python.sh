#!/bin/bash

mkdir -p pb

python -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. pb/helloworld.proto
