# Code-portfolio
This is a place to show what sort of code I write.

### phisherDetector
It was suggested to me that I should write a method using natural language processing, recursive webpage scraping, and neural networks to automatically scan and distinguish two sets of websites. The result is a set of 5 interlocking scripts, a data pipeline which: 
1. scrapes the target's web corpus recursively, 
2. repeats for a counter-sample of related links, 
3. tokenizes the differences in their writing, and then 
4. trains a neural network to distinguish between the two.

I proposed the project as a procedural, scalable way to scan the internet for pages phishing the users of a given website. Once the distinguishing neural network is produced, it can distinguish any vectorized text automatically, flagging websites for review as potential phishing sites, for any web property.

#### Performance:
Set to recursively scrape links starting from https://rapid7.com and including 'rapid7' in their link structure, and with a preset limit of 10,000 links, it found and successfully scraped visible text from 5384 in-network links and 1301 out-network links. The next script vectorized the text into 40 keywords, 4 sentiment analysis variables and sentence length in words. Trained on the resulting vector in Tensorflow with GPU acceleration, this produced the neural network 'rapid7.10000.h5', with accuracy 88.1%, (38.1% above chance) in 7 minutes of training. This process is meant to be a general use tool, which should work for any client website.

You can see the details of the keyword analysis, as well as the accuracy and completion time of the produced neural networks, in the logfile ClassifierLog.txt. The scripts, as well as the vector csv and neural network produced, are uploaded here. 

### cricket-elasticsearch:
As part of an interview process I was given a code challenge to write a scoring system for the dart game Cricket, which included detailed application of the rules, supported variable teams, variable text inputs, and runs a little local elasticsearch server to keep player records, and reference them in-game. I like it because it's a single script which is a self-contained network of interlocking functions, which are only able to generate data and outputs they can handle. It simulates the dart game 'Cricket', which was new to me, so I figured it out by watching this video: https://www.youtube.com/watch?v=odKhntmqiHw&t

It runs an elasticsearch server to record names of previous users, and wins and losses. When it first runs it auto-populates the server like an old-school arcade game, displaying a list of 'Top Three Cricket Masters' at the beginning, and then if you rack up the wins you can get on that list too. The server is persistent on your own machine, so you can close the python program and come back to find your old character data still there.

### TwitterClassifier: 
This uses a neural network to attempt to classify the writer of text from two different Twitter users.
It does the following:
1. extracts Tweets from target users, 
2. vectorizes those Tweets using NLTK,
3. uses those vectors to train a TensorFlow neural network to distinguish between the two Tweet sources.

#### Performance: 
The first version, TwitterClassifier.v.1.py, was tasked with distinguishing tweets from Donald Trump's twitter feed from those in Jill Stein's. This script yielded network 'realDonaldTrump.DrJillStein.07202018.h5', with accuracy 0.6768, after 3 hours running the neural network training cycle. The script currently only goes to the point at which the network is generated; After this point there is a separate script to initiate the predictions and tests.

I updated the code to TwitterClassifier.v.2.py, which expanded the keyword lists and also includes Vader sentiment analysis, and targeted Shaquille O'Neal and Neil DeGrasse Tyson. It learned much more quickly, producing 'neiltyson.SHAQ.07232018.h5' with accuracy 0.754 within ten minutes.

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
