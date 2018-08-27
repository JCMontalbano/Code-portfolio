### FDlookup.py:
See the writeup at my blog here: http://www.eosmath.com/2018/06/fire-department-lookup-whos-within-8.html

This is a project I completed for Austin's city government. They needed to determine how many people were more than 8 minutes from the nearest fire department. I produced a CSV with coordinates, and several images visualizing the results.
This script uses three data inputs: 
1. 'FD.csv', a list of lat/lon coordinates for Austin Fire Department stations
2. 'ATXsearch.csv', a grid, ~0.1KM in resolution, of points inside the Austin city limits. I produced this separately. 
3. 'popgrid.csv', a grid, ~0.1KM in resolution, of population density in North America.

The script goes through each point of the ATXsearch list, determines the nearest FD station, and uses Google Maps API to calculate the time of arrival. It accepts arguments for time of day and day of week, and I used it to produce maps of times with high traffic congestion, i.e. Wednesday at 8AM and 5PM, etc. The delay value in seconds I then multiplied by the value of that point in the population grid, yielding a 'person-seconds' metric. This visualizes where the most people are affected by the largest delays. 

I produced the image below using QGIS. I removed all points where the delay was less than the target time, and presented the remaining points colored in a white-blue gradient for the person-seconds metric. The darker blue areas show the largest delays, the red dots are the fire departments. The data objects produced, as well as the map images, are in this repo.
!['Friday at 5PM'](https://raw.githubusercontent.com/JCMontalbano/Code-portfolio/master/FDlookup/Friday5PFDsmall.jpg)
