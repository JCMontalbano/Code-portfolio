This project searches two twitter user's timelines, vectorizes their tweets with NLTK, and uses TensorFlow to train a neural network to distinguish between them.

#### TwitterClassifier.v.1.py: 
The first version, produced the neural network realDonaldTrump.DrJillStein.07202018.h5 and the log file SteinTrumpLog.txt.

This version searches each target timeline for 5 key words, and then trains a neural network to a target threshold.

#### TwitterClassifier.v.2.py: 
Produced the neural network neiltyson.SHAQ.07232018.h5 and the log file NeilShaqLog.txt.

This version counts each tweet for 10 unique key words from each source (20 keywords total), and includes Vader sentiment analysis. It worked faster.

#### Future features:
* counter-filtering between the two lists.
* post-training network performance validation on new data
