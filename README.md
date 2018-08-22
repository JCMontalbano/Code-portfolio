# Code-portfolio
This is a place to show what sort of code I write.

### TwitterClassifier: 
This uses a neural network to attempt to classify the writer of text from two different Twitter users.
It does the following:
1. extracts Tweets from target users, 
2. vectorizes those Tweets using NLTK,
3. uses those vectors to train a TensorFlow neural network to distinguish between the two Tweet sources.
#### Performance: 
The first version, TwitterClassifier.v.1.py, was tasked with distinguishing tweets from Donald Trump's twitter feed from those in Jill Stein's. This script yielded network 'realDonaldTrump.DrJillStein.07202018.h5', with accuracy 0.6768, after 3 hours running the neural network training cycle. The script currently only goes to the point at which the network is generated; After this point there is a separate script to initiate the predictions and tests.

I updated the code to TwitterClassifier.v.2.py, which expanded the keyword lists and also includes Vader sentiment analysis, and targeted Shaquille O'Neal and Neal DeGrasse Tyson. It learned much more quickly, producing 'neiltyson.SHAQ.07232018.h5' with accuracy 0.754 within ten minutes.

### FDlookup:
See the writeup at my blog here: http://www.eosmath.com/2018/06/fire-department-lookup-whos-within-8.html

This is a project I completed for Austin's city government. They needed to determine how many people were more than 8 minutes from the nearest fire department. I produced a CSV with coordinates, and several images visualizing the results.
This script uses two data inputs: 
1. 'FD.csv', a list of lat/lon coordinates for Austin Fire Department stations
2. 'ATXsearch.csv', a grid, ~0.1KM in resolution, of points inside the Austin city limits. I produced this separately. 

The script goes through each point of the ATXsearch list, determines the nearest FD station, and uses Google Maps API to calculate the time of arrival. It accepts arguments for time of day and day of week, and I used it to produce maps of times with high traffic congestion, i.e. Wednesday at 8AM and 5PM, etc.The data objects produced, as well as the map images, are in this repo.

### NASDAQ Study:
This was a project to detect when a group of prices moves together, relative to the background motion of their market.
**stockScrapeIEX.py** scrapes stock data for a target group of stocks and a randomly selected control group of stocks, over a target date range. It then vectorizes them into daily percent change values, and stores the vectors as small CSVs.
**compareVector.py** accepts the CSVs from above, analyzes them, and produces an image file comparing them with a novel metric. It highlights each day with a vertical red bar, whose color saturation is determined by the ratio of (target group average vector):(control group average vector). This produces a direct visual measure of when a group of stocks is moving together relative to the market.

### cricket-elasticsearch:
This is the biggest and most complicated thing I've done that isn't under NDA, I like it because it's a single script which is a self-contained network of interlocking functions, which are only able to generate data and outputs they can handle. It simulates the dart game 'Cricket', which was new to me, so I figured it out by watching this video: https://www.youtube.com/watch?v=odKhntmqiHw&t
It runs an elasticsearch server to record names of previous users, and wins and losses. When it first runs it auto-populates the server like an old-school arcade game, displaying a list of 'Top Three Cricket Masters' at the beginning, and then if you rack up the wins you can get on that list too. The server is persistent on your own machine, so you can close the python program and come back to find your old character data still there.
