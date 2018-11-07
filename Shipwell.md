## Shipwell Predictive Routing Research Proposal:

We can compete well with other 3PLs by solving for the KPIs of the shippers and the truckers. Truckers want to maximize income per mile driven, while satisfying requirements like the 80/7 rule; shippers want to minimize cost per mile while satisfying time requirements. If we analyze your event data for recurring cycles - i.e. weekly, monthly, seasonal and yearly recurring trends in demand, we can model the demand geospatially across our grid. With a map of future demand, we can improve our service in several ways.

**For a working iPython notebook of my code using curve-fitting to model a weekly trend in a single variable, see here:** [RideAustinPolynomial](https://github.com/JCMontalbano/Code-portfolio/tree/master/RideAustinPolynomial)

**For a writeup modeling and visualizing a daily trend from historical data in a datetime and latitude/longitude context, see here:** 
[Ride|Austin Saturday Traffic Distribution](http://www.eosmath.com/2017/05/rideaustin-saturday-traffic-distribution.html)

Having identified time and geospatial trends in your shipping data, we can predict (with some uncertainty) the future value of a trucker's position at the end of their transit time. This allows us to route truckers toward positions which will keep them working on the next job or back haul. We can then direct our trucks toward regions which have a large number of possible or likely jobs, even before we've received orders for these jobs. If truckers can count on Shipwell to route them toward reliable work, they can neglect other 3PLs, and we acquire a larger workforce to offer our shippers, which in turn improves the performance we can offer to them.

I've already implemented a mathematically similar solution at [Ridemap](https://ridemap.ai). Ridemap's map is a 6 dimensional histogram of historical rideshare data, displayed as a heatmap sliced for current time and date, where two dimensions are lat/lon, three are positions in the time cycles, and one is the dependent variable. Ridemap's 'auto-navigate' feature involves a weighted k-means cluster implemented in React for Android and iOS. Shipwell doesn't need to implement it in the mobile app, but since React is in Java, it implies we can easily implement similar math in Java or even C, depending on what Shipwell's servers run. I've also written it in Python. 

**For a great little animation explaining the K-means cluster algorithm (0:59), click here:** [k-means clustering](https://www.youtube.com/watch?v=5I3Ei69I40s). This unsupervised algorithm identifies naturally occuring centers in data, and works well in lat/lon context. 

**For an example of using k-means clusters to successfully predict stochastic demand centers from a historical record, see here:** [K-Means Clustering of Rideshare providers leads to better performance; how an Austin startup can compete with the giants using machine learning
](http://www.eosmath.com/2017/06/k-means-clustering-of-rideshare.html)

### Modeling your data in this way allows the following features:
* Identify demand time cycles independently per-shipper, and combine for changing predictive demand maps. As you acquire more data, you can update predictions continuously.
* Solve for 80/7 and 34-hour restart times in our predictive routing. For trucking firms with more drivers than trucks, we can help the trucks constantly run even when the drivers have downtime, and solve for the back transport of the displaced drivers as well.
* incentivize LTL shippers with procedurally reduced Shipwell markup to fill our trucks predictively to approach FTL cost-per-mile efficiency. This maximizes the trucks' back haul income, further encouraging them to reduce their use of other 3PLs. We can match NMFC code and slice the map for that demand predictively as well.
* We can monitor when and where trucks drop in and out of availability to detect our 3PL competitor's freight patterns, and direct our sales teams towards shippers in those areas at those times. We can also model this using time anomalies in LTL freight shipping transit time, allowing us to infer other orders.
* Predict 34-hour restart time and allow truckers to route toward more desirable locations on their weekends, including custom results for specific firms, including a desire to route toward their homes, and even accomodating truckers desiring to gravitate to multiple home bases with separate target times.
