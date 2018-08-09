### NASDAQ Study:
This was a project to detect when a group of prices moves together, relative to the background motion of their market.
**stockScrapeIEX.py** scrapes stock data for a target group of stocks and a randomly selected control group of stocks, over a target date range. It then vectorizes them into daily percent change values, and stores the vectors as small CSVs.
**compareVector.py** accepts the CSVs from above, analyzes them, and produces an image file comparing them with a novel metric. It highlights each day with a vertical red bar, whose color saturation is determined by the degree to which the prices are moving together. This produces a direct visual measure of when a group of stocks is moving together relative to the market.

In the first picture, I wanted to assess the value of news stories in the format '[group of stocks] plunge in response to [event]'. I found the following story: https://www.cnbc.com/2017/06/29/us-stocks-fall-tech-banks.html

So I pulled the FANG stocks as a target group, over the month of July. **stockScrapeIEX.py** accepts a list of stocks as an argument, as well as a delay value, a keyword, and start and end dates, so the command looks like:

```
python3 stockScrapeIEX.py JulyFANG 5 'FB AMZN NFLX GOOGL TWTR SNAP' '2018-07-01' '2018-08-06'
```

I then ran **compareVector.py** on the result, which just needed the keyword now:

```
python3 compareVector.py JulyFANG 
```

This produced image JulyFANG.png:
!['JulyFANG Vectors'](https://raw.githubusercontent.com/JCMontalbano/Code-portfolio/master/NASDAQStudy/JulyFANG.png)

#### Implications for future research:
The most valuable part of this is the new metric. Separated from this code, I'd like to run it in a naive way over all the small groups, combinatorically, and identify groups which tend to move together over time. I like the way the image turned out, but this algorithm will scale well into really massive treatments, and that's what's most valuable.
