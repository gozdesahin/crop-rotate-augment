mkdir ./data
cd data

# Download UD-treebank v2.1
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2515{/ud-treebanks-v2.1.tgz}

# extract the treebank
tar -xvzf ud-treebanks-v2.1.tgz

# delete all unnecessary stuff
find . -type f -name  '*.txt' -delete

echo "Ready to go"

