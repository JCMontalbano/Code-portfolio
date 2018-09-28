# DNAclassifier
I combined NLP classifier code with bioinformatics code, to identify recurring DNA motifs in reference genomes and train a neural network to classify between the two samples.

1. 1.learnMotifs.py studies two reference genomes and identifies the top 100 recurring motifs, at specified lengths
2. 2.tokenizeFastQ.py works for fastA or fastQ raw data formats, and tokenizes it using the motifs from 1
3. 3.trainDNAclassifier.py accepts the tokenized data from 2 and trains a neural network to classify between the two.

This gives a procedural, scalable data pipeline which can automatically identify microbial samples right from the Illumina machine.

### Features:
* The motif search can be run ahead of time, using reference data from [NCBI's ftp database(ftp://ftp.ncbi.nih.gov/genomes/archive/old_refseq/Bacteria/)
* Motif base-pair length, sample depth, and the neural network's target accurcy thresholds can be readily tweaked with hardcoded variables.
* The code can be adapted to distinguish between more than 2 types of bacteria sample, and give partial reads from several reference datasets, to identify transgenic genomes

### Implications for future development:
* We should run the motif searches ahead of time to develop a large library, and set of front-end tools
* The pipeline presently only runs up to the training of the network, but it needs at least one more script to test new data.
* Because the Metasploit product is still presented partially as a separate brand from rapid7, 'rapid7' isn't found in its links, meaning this process missed the Metasploit web structure. It can be easily modified to include multiple keywords in these instances.

# Script chain:
Before using the .fna files from the reference set, they must be reduced to a single line, using the following bash code:
```
sed -i -e '1d' $REF_FILE #strips the first line
tr -d '\n' < $REF_FILE > $FILE2 #removes linebreaks
cat $FILE2>>$motif_file #if you wish to combine multiple reference files
```
After this process, the script chain can be run in bash as follows:
```
python3 1.learnMotifs.py ecoli1.fna paerug1.fna ecolimotifs1020.csv paerugmotifs1020.csv
python3 2.tokenizeFastQ.py ecolimotifs1020.csv paerugmotifs1020.csv Ecoli.FLX.fna paerug1.fastq ecoli.paerug.full.csv 0
python3 3.trainDNAClassifier.py ecoli.paerug.full.csv ecoli.paerug.h5
```
It is quite possible to refactor this code to run in a single lightweight bash script which runs start to finish without generating the intermediate data objects, and which could be made to run on the cloud. 

## 1.learnMotifs.py
```
python3 1.learnMotifs.py ecoli1.fna paerug1.fna ecolimotifs1020.csv paerugmotifs1020.csv
```
Learn the recurring motifs from single-line FNA. The first two arguments are for the sample files, produced using the bash script above. The second two arguments are the output datasets. This script doesn't actually need to run on two reference datasets, but it presently does to make the binary comparison complete and self-contained. The output files are CSVs drawn from a Pandas dataframe which contains the most frequently recurring motifs from each sample. Can generate motifs of different lengths.

## 2.tokenizeFastQ.py
```
python3 2.tokenizeFastQ.py ecolimotifs1020.csv paerugmotifs1020.csv Ecoli.FLX.fna paerug1.fastq ecoli.paerug.full.csv 0
```
Tokenize the raw data inputs, using the motif lists from part 1. The raw data used here is from the [Qiagen sample data site](https://www.qiagenbioinformatics.com/support/example-data/). Because individual raw data reads are quite short (~100-300 base-pairs), this script combines 1,000 reads before tokenizing, which yields robust feature counts. The last variable is an integer which determines how many reads to test.

## 3.trainDNAClassifier.py
```
python3 3.trainDNAClassifier.py ecoli.paerug.full.csv ecoli.paerug.h5
```
This script loads the vectorDF from 2.tokenizeFastQ.py and then trains a neural net to distinguish the two, using TensorFlow and Keras. It cycles through a set of hyperparameters which I've found typically work for binary classifier problems like this.
The script loads motif vectors produced in 2 as a target array.
It selects a random 20% of array, 50% class balanced, loads it as training data, and trains a network. The neural network uses hyperparameters hardcoded at the beginning of the script, and has an adaptible accuracy threshold which can be set to slowly decrement target accuracy until you get a network at the target accuracy threshold.
When it trains a neural network at the target accuracy, it saves it, logs it and ends.
