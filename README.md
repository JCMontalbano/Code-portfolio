# Code-portfolio
This is a place to show what sort of code I write. I also did the analysis at https://ridemap.ai

### phisherDetector
It was suggested to me that I should write a method using natural language processing, recursive webpage scraping, and neural networks to automatically scan and distinguish two sets of websites. The result is a set of 5 interlocking scripts, a data pipeline which: 
1. scrapes the target's web corpus recursively, 
2. repeats for a counter-sample of related links, 
3. tokenizes the differences in their writing, and then 
4. trains a neural network to distinguish between the two.

I proposed the project as a procedural, scalable way to scan the internet for pages phishing the users of a given website. Once the distinguishing neural network is produced, it can distinguish any vectorized text automatically, flagging websites for review as potential phishing sites, for any web property.

### FDlookup:
See the writeup at my blog here: http://www.eosmath.com/2018/06/fire-department-lookup-whos-within-8.html

This is a project I completed for Austin's city government. They needed to determine how many people were more than 8 minutes from the nearest fire department. I produced a CSV with coordinates, and several images visualizing the results. The script goes through each point of the ATXsearch list, determines the nearest FD station, and uses Google Maps API to calculate the time of arrival.

### NASDAQ Study:
This was a project to detect when a group of prices moves together, relative to the background motion of their market.
**stockScrapeIEX.py** scrapes stock data for a target group of stocks and a randomly selected control group of stocks, over a target date range. It then vectorizes them into daily percent change values, and stores the vectors as small CSVs.
**compareVector.py** accepts the CSVs from above, analyzes them, and produces an image file comparing them with a novel metric. It highlights each day with a vertical red bar, whose color saturation is determined by the ratio of (target group average vector):(control group average vector). This produces a direct visual measure of when a group of stocks is moving together relative to the market.

### RideAustinPolynomial:
PolynomialWeekly.ipynb is a Jupyter Notebook analysis of RideAustin's daily ride request volume, identifying a weekly cycle. The data released covers rides requested from June 16 to August 31, just over 11 weeks. It shows a clear cycle weekly, typically with peak ride demand on Saturday. I model this cycle as a spliced set of 7 polynomial curve fits and achieve close fit.

### cricket-elasticsearch:
I was given a code challenge to write a scoring system for the dart game Cricket, which included detailed application of the rules, supported variable teams, variable text inputs, and runs a little local elasticsearch server to keep player records, and reference them in-game. I like it because it's a single script which is a self-contained network of interlocking functions, which are only able to generate data and outputs they can handle.
