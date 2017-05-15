#!/bin/bash
export TF_CONFIG='{
  "cluster": {
    "ps": ["localhost:9999"],
    "master": ["localhost:9998"],
    "worker": ["localhost:9998", "localhost:9997"]
  },
  "environment": "cloud",
  "task": {
     "type": "master",
     "index": 0
  }
}'

python boston_house_dist.py
