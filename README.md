# Code-portfolio
This is a place to show what sort of code I write.

### TwitterClassifier.py: This uses a neural network to attempt to classify the writer of text from two different Twitter users.
It does the following:
1. extracts Tweets from target users, 
2. vectorizes those Tweets using NLTK,
3. uses those vectors to train a TensorFlow neural network to distinguish between the two Tweet sources.
#### Criticism of this code: 
I haven't had time to do a parameter grid-search, so presently it's 
training the network using parameters I found from a separate grid search. Regrettably, they don't
work very well for this material, so while the code runs properly, it doesn't yet train a satisfying net.

### FDlookup.py: This is a project I completed for Austin's city government. They needed to determine how many 
people were more than 8 minutes from the nearest fire department. I produced a CSV with coordinates, and 
several images visualizing the results.
This script uses two data inputs: 
1. 'FD.csv', a list of lat/lon coordinates for Austin Fire Department stations
2. 'ATXsearch.csv', a grid, ~0.1KM in resolution, of points inside the Austin city limits. I produced this separately.
The script goes through each point of the ATXsearch list, determines the nearest FD station, and uses
Google Maps API to calculate the time of arrival. It accepts arguments for time of day and day of week, 
and I used it to produce maps of times with high traffic congestion, i.e. Wednesday at 8AM and 5PM, etc.
The data objects produced, as well as the maps, are in this repo.
