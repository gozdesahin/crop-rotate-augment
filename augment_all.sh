#!/bin/sh
export PYTHONIOENCODING=utf-8

python augment_benchmark.py \
   -input "./data/ud-treebanks-v2.1" \
   -maxrot 3 \
   -prob 0.3
