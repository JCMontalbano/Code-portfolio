#python3 FDlookup.py FDlookup.csv '6-1-2018 8:00'
import numpy as np
import pandas as pd
import shapefile
from shapely.geometry import shape, Point
import googlemaps
import sys
from scipy.spatial import cKDTree
import datetime

output=sys.argv[1]
Departure=datetime.datetime.strptime(sys.argv[2],'%m-%d-%Y %H:%M')
client=googlemaps.Client('AIzaSyCNt49hOveezLgHFg2DSV5ATmSZLy13JYg')

def do_kdtree(combined_x_y_arrays,points):
    mytree = cKDTree(combined_x_y_arrays)
    #mytree = scipy.spatial.cKDTree(combined_x_y_arrays)
    dist, indexes = mytree.query(points) #but we don't need dist, its in lat/lon anyway
    return indexes

def TravelTime(lng1,lat1,lng2,lat2,Departure):
	#use Distance Matrix GMAPI to get travel time, in s, from point 1 to 2
	StartCoordinates=(lat1,lng1)
	EndCoordinates=(lat2,lng2)
	result=client.distance_matrix((EndCoordinates),(StartCoordinates), departure_time=Departure)
	Time=result['rows'][0]['elements'][0]['duration']['value'] 
	return Time

print('Loading points...')
pointsDF=pd.read_csv('ATXsearch.csv', index_col=0)
pointsy=pointsDF['lat'];pointsx=pointsDF['lng']
pointsarray=np.dstack([pointsy.ravel(),pointsx.ravel()])[0]
#import coordinates of the FDs from Michael, massage data
FDF=pd.read_csv('FD.csv')
FDy=FDF['Y']
FDx=FDF['X']
FDy=np.array(FDF['Y'])
FDx=np.array(FDF['X'])
FDarray=np.dstack([FDy.ravel(),FDx.ravel()])[0]

print('Indexing nearest neighbors...')
indices = do_kdtree(FDarray,pointsarray)

FDlatlist=[]
FDlnglist=[]
#FDindex=np.empty([0,2], dtype=float)
for X in indices:
	lat=FDarray[X][0]
	lng=FDarray[X][1]
	FDlatlist.append(lat)
	FDlnglist.append(lng)
    #FDindex=np.append(FDarray, [np.array(FDarray.loc[X,:])], axis=0) #what's this look like

gridlistDF=pointsDF
gridlistDF['FDlng']=FDlnglist
gridlistDF['FDlat']=FDlatlist
#now do the Distance Matrix calls

#DTlist=#initialize a list of times
#for DT in DTlist:

DT=Departure#for what time of day?
backupcount=0
#timelist=[]

finalDF=pd.DataFrame(columns=['lng','lat','time'])

print('Looking up times...')
for row in gridlistDF.iterrows():
	lng=row[1][0]
	lat=row[1][1]
	FDlng=row[1][2]
	FDlat=row[1][3]
	time=TravelTime(FDlng,FDlat,lng,lat,DT) #going from FD to target
	print('FD:('+str(FDlat)+','+str(FDlng)+') target:('+str(lat)+','+str(lng)+'): '+str(time)+' seconds')
	print(str(backupcount/len(gridlistDF))+' percent complete')
	#timelist.append(time)
	row=[lng,lat,time]
	print(row)
	finalDF.loc[len(finalDF)]=row				
	backupcount+=1
	if backupcount%50==0:
		finalDF.to_csv(output)
		print('Backing up output at row #:'+str(backupcount))


outputDF=gridlistDF.drop(['FDlng','FDlat'], axis=1)
outputDF['time']=timelist
outputDF.to_csv(output)
print('Done!')