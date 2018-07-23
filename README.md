# Code-portfolio
This is a place to show what sort of code I write.

### TwitterClassifier.py: 
This uses a neural network to attempt to classify the writer of text from two different Twitter users.
It does the following:
1. extracts Tweets from target users, 
2. vectorizes those Tweets using NLTK,
3. uses those vectors to train a TensorFlow neural network to distinguish between the two Tweet sources.
#### Performance: 
In the first test, tasked with distinguishing tweets from Donald Trump's twitter feed from those in Jill Stein's, this script yielded network 'realDonaldTrump.DrJillStein.07202018.h5', with accuracy 0.6768, after 3 hours running the neural network training cycle. The script currently only goes to the point at which the network is generated; After this point there is a separate script to initiate the predictions and tests.
I updated the code to TwitterClassifier.v.2.py, which now includes Vader sentiment analysis, and targeted Shaquille O'Neal and Neal DeGrasse Tyson. It learned much more quickly, producing neiltyson.SHAQ.07232018.h5 with accuracy 0.754 within ten minutes.

### FDlookup.py:
See the writeup at my blog here: http://www.eosmath.com/2018/06/fire-department-lookup-whos-within-8.html

This is a project I completed for Austin's city government. They needed to determine how many people were more than 8 minutes from the nearest fire department. I produced a CSV with coordinates, and several images visualizing the results.
This script uses two data inputs: 
1. 'FD.csv', a list of lat/lon coordinates for Austin Fire Department stations
2. 'ATXsearch.csv', a grid, ~0.1KM in resolution, of points inside the Austin city limits. I produced this separately. 

The script goes through each point of the ATXsearch list, determines the nearest FD station, and uses Google Maps API to calculate the time of arrival. It accepts arguments for time of day and day of week, and I used it to produce maps of times with high traffic congestion, i.e. Wednesday at 8AM and 5PM, etc.The data objects produced, as well as the map images, are in this repo.
!['Friday at 5PM'](https://raw.githubusercontent.com/JCMontalbano/Code-portfolio/master/FDlookup/Friday5PFDsmall.jpg)
