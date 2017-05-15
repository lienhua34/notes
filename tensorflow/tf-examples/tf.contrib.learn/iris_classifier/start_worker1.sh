#!/bin/bash
export TF_CONFIG='{
  "cluster": {
    "ps": ["localhost:9999"],
    "worker": ["localhost:9998", "localhost:9997"]
  },
  "environment": "local", 
  "task": { 
     "type": "worker", 
     "index": 1 
  }
}'

python iris.py
