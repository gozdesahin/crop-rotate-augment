# crop-rotate-augment

The code for our EMNLP18 paper "Data Augmentation via Dependency Tree Morphing for Low-Resource Languages". 

First you need to download UD treebanks v2.1. You can do so by running '**sh preprocess.sh**'
Then you can either experiment with the method parameters and single connlu files by running '**sh augment_single.sh**'. File parameters are:
- **infile**: UD file to augment
- **outfile**: Name of the output file
- **maxrot**: Maximum number of rotations per sentence
- **prob**: Probability of the augmentation operation
- **operation**: rotate or crop

We also provide the script, **augment_all.sh** to augment all training UD files. The parameters are:
- **input**: Root folder where UD treebanks are downloaded (e.g., ./data/ud-treebanks-v2.1)
- **maxrot**: Maximum number of rotations per sentence
- **prob**: Probability of the augmentation operation

Beware that this is Python 2.7 code! 
