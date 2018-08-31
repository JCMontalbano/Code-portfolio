# phisherDetector
It was suggested to me that I should write a method using natural language processing, recursive webpage scraping, and neural networks to automatically scan and distinguish two sets of websites. The result is a set of 5 interlocking scripts, a data pipeline which scrapes the target's web corpus recursively, repeats for a counter-sample of related links, tokenizes the differences in their writing, and then learns to distinguish between the two.
I proposed the project as a procedural, scalable way to scan the internet for pages phishing the users of a given website. Once the distinguishing neural network is produced, it can distinguish any vectorized text automatically, flagging websites for review as potential phishing sites, for any web property.

### Performance:
Instructed to find all networks starting from https://rapid7.com and including 'rapid7' in their link structure, and with a preset limit of 10,000 links, it found and successfully scanned 5384 in-network links and 1301 out-network links. The next script vectorized the text into 40 keywords, 4 sentiment analysis variables and sentence length in words. Trained on the resulting vector in Tensorflow with GPU acceleration, this produced the neural network 'rapid7.10000.h5', with accuracy 88.1%, (33.1% above chance) in 7 minutes of training. This process will absolutely scale into easy mass use.

You can see the details of the keyword analysis, as well as the accuracy and completion time of the produced neural networks, in the logfile ClassifierLog.txt. The scripts, as well as the vector csv and neural network produced, are uploaded here. 

### Features:
*The project keeps performance logs in ClassifierLog.txt
*Filenames are dynamically generated with data objects at each step of the process.
*The neural network's target accurcy thresholds can be readily tweaked with hardcoded variables.

### Implications for future research:
* This project focused entirely on text vectors for analysis, but a phisher would also likely be using the targets proprietary imagery, css, and other website features as well. All of this can be vectorized and used to make the network smarter.
* Detached from the recursive link scraper in parts 0-2, the code for vectorizing text and training a neural network to distinguish it is immediately applicable to the task of distinguishing *any* two bodies of text. Particularly this could be a new feature recognizing phishing emails.

# Script chain:
The entire chain can be run in a bash script as follows:
```
python3 0.recursivelinkscrape.py https://rapid7.com rapid7 10000 
python3 1.recursiveTextScan.py https://rapid7.com rapid7 10000
python3 2.countersample.py rapid7 10000
python3 3.vectorizeText.py rapid7 10000
python3 4.trainClassifierNetwork.py rapid7 10000
```
## 0.recursivelinkscrape.py
search rapid7 structure to gather 10,000 links:
```
python3 0.recursivelinkscrape.py https://rapid7.com rapid7 10000 
```
This segment scrapes the target webpage for hyperlinks containing the target keyword.
It recursively finds the webpage, and also finds github properties, offsite hosted libraries, etc. which are still a structured part of the organization's internet presence, i.e. https://travis-ci.org showing up for rapid7. 
I blacklisted web.archive.org because it prevents the unlimited scan from terminating. Further development will surely yield other such scanner-attractors for the blacklist feature.
The scraper also finds procedurally generated lists; we could probably procedurally solve their list generating protocols from this data.

The next step with this data is in 1.recursiveTextScan.py, which collects the visible text from these links. You don't actually need to run script 0.recursivelinkscrape.py, but it runs much faster than 1.recursiveTextScan.py because it's not doing as much. This is a preliminary scan.

This script preserves the outward-pointing link list as a procedurally generated csv the name from the procedurally generated outlink csv is used as a cue in the next stage, when I use the outlinks to pull a list of related ngrams as a counter-filter for the most common ngrams in the rapid7 site; this allows to avoid false positives on near-industry links by targeting word choices specific to the target company.

## 1.recursiveTextScan.py
```
python3 1.recursiveTextScan.py https://rapid7.com rapid7 10000
```
this script scans the visible text of the in-network links and saves it in the procedurally named output, which is a csv with two columns, link and its visible text.

## 2.countersample.py
```
python3 2.countersample.py rapid7 10000
```
This script does the same text scan as in 1.recursiveTextScan.py, but now it is scanning the out-of-network links generated before.

## 3.vectorizeText.py
```
python3 3.vectorizeText.py rapid7 10000
```
This script takes the text scans from 1.recursiveTextScan.py and 2.countersample.py, word-tokenizes them, counts the most frequently occurring 1, 2, 3 and 4 word phrases, eliminates duplicates, producing a list of 40 key ngrams. It then goes through each list of text scans, counting key phrases and performing sentiment analysis. Each entry is tagged as coming from the in network or out-network scan with a binary value, 'whichCorpus'. The resulting two vectorized DFs are concatenated and saved to a single file, vectorOutput.

## 4.trainClassifierNetwork.py
```
python3 4.trainClassifierNetwork.py rapid7 10000
```
This script loads the vectorDF from 3.vectorizeText.py and then trains a neural net to distinguish the two, using TensorFlow and Keras. It cycles through a set of hyperparameters which I've found typically work for binary classifier problems like this.
The script loads NLTK vectors produced in 3.vectorizeText.py as a target array.
select random 20% of array, 50% class balanced, load it as training data, and train a network.The neural network uses hyperparameters set at the beginning, and has an adaptible accuracy threshold which can be set to slowly decrement target accuracy until you get a network at the target accuracy threshold.
