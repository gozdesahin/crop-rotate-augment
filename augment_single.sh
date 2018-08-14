#!/bin/sh
export PYTHONIOENCODING=utf-8

echo "Testing rotation"
python augment.py \
   -infile "./data/ud-treebanks-v2.1/UD_Turkish/tr-ud-test.conllu" \
   -outfile "./data/ud-treebanks-v2.1/UD_Turkish/rotated-tr-test.conllu" \
   -maxrot 3 \
   -prob 0.3 \
   -operation "rotate"

echo "Testing cropping"
python augment.py \
   -infile "./data/ud-treebanks-v2.1/UD_Turkish/tr-ud-test.conllu" \
   -outfile "./data/ud-treebanks-v2.1/UD_Turkish/cropped-tr-test.conllu" \
   -prob 0.3 \
   -operation "crop"

echo "Done, check your output files"
