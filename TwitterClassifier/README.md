This project searches two twitter user's timelines, vectorizes their tweets with NLTK, and uses TensorFlow to train a neural network to distinguish between them.

#### TwitterClassifier.v.1.py: 
The first version, produced the neural network realDonaldTrump.DrJillStein.07202018.h5 and the log file SteinTrumpLog.txt.

This version counts each tweet for 10 unique key words from each source (20 keywords total), and then trains a neural network to a target accuracy threshold.

#### TwitterClassifier.v.2.py: 
Produced the neural network neiltyson.SHAQ.07232018.h5 and the log file NeilShaqLog.txt.

This version includes Vader sentiment analysis. It worked faster, but it had different targets.

#### Future features:
* counter-filtering between the two keyword lists.
* post-training network performance validation on new data
